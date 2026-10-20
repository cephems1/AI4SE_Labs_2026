"""Graph nodes and routing functions.

LLM (agentic) nodes:    extract, completeness_check, build_taxonomy, consolidate, review, revise
Deterministic nodes:    load_corpus, collect_round, coverage_gate, validate, render
"""

import re
from difflib import get_close_matches

from langgraph.types import Send

from . import prompts as P
from .config import (CHUNK_CHARS, MAX_CONSOLIDATION_ROUNDS, MAX_EXTRACTION_ROUNDS, MAX_NAME_WORDS,
                     MAX_REVIEW_ROUNDS, MIN_DESCRIPTION_WORDS, PRIORITY_LEVELS)
from .corpus import chunk_documents, is_grounded, load_documents
from .llm import call_structured, log
from .render import render_outputs
from .schemas import (CompletenessReport, ConsolidationResult, ExtractionResult, ReviewResult,
                      RevisionResult, TaxonomyResult)


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------
def _doc_register(documents: list[dict]) -> str:
    return "\n".join(f"- {d['doc_id']}: {d['path']} (date: {d['date']})" for d in documents)


def _glossary_text(taxonomy: dict) -> str:
    lines = []
    for g in taxonomy["glossary"]:
        avoid = f" [avoid: {', '.join(g['avoid'])}]" if g["avoid"] else ""
        lines.append(f"- {g['term']}: {g['definition']}{avoid}")
    return "\n".join(lines) or "(none)"


def _candidate_block(c: dict, docs_by_id: dict) -> str:
    doc = docs_by_id[c["doc_id"]]
    flags = []
    if c["suspicious"]:
        flags.append(f"SUSPICIOUS: {c['suspicion_note']}")
    if not c["grounded"]:
        flags.append("quote not found verbatim in source")
    flag_text = f" | {'; '.join(flags)}" if flags else ""
    return (f"- {c['candidate_id']} | {c['doc_id']} ({doc['path']}, {doc['date']}) | stakeholder: {c['stakeholder']} "
            f"| {c['req_type']} | priority signal: {c['priority_signal']}{flag_text}\n"
            f"  statement: {c['statement']}\n  quote: \"{c['quote']}\"")


def _req_line(r: dict, full: bool = True) -> str:
    text = r["description"] if full else r["description"][:200]
    return f"- {r['id']} [{r['area']}] {r['priority']} {r['req_type']} | {r['name']}: {text}"


def _sources_of(candidate_ids, cand_by_id: dict) -> list[str]:
    return sorted({cand_by_id[c]["doc_id"] for c in candidate_ids if c in cand_by_id})


# ---------------------------------------------------------------------------
# 1. load_corpus (deterministic)
# ---------------------------------------------------------------------------
def load_corpus(state: dict) -> dict:
    docs = load_documents(state["input_dir"])
    chunks = chunk_documents(docs, CHUNK_CHARS)
    log(f"load_corpus: {len(docs)} documents, {len(chunks)} chunks from {state['input_dir']}")
    return {"documents": docs, "chunks": chunks, "extraction_round": 0,
            "active_chunks": [c["chunk_id"] for c in chunks], "consolidation_round": 0, "review_round": 0}


def fan_out_extraction(state: dict):
    return [Send("extract", {"chunk": c, "round": 0, "missed": [], "already": []}) for c in state["chunks"]]


# ---------------------------------------------------------------------------
# 2. extract (LLM, one task per chunk, parallel)
# ---------------------------------------------------------------------------
def extract(payload: dict) -> dict:
    chunk, rnd = payload["chunk"], payload["round"]
    feedback = ""
    if payload["missed"]:
        feedback = P.EXTRACT_FEEDBACK.format(
            already="\n".join(f"- {s}" for s in payload["already"]) or "(none)",
            missed="\n".join(f"- {m['description']} (quote: \"{m['quote']}\")" for m in payload["missed"]),
        )
    user = P.EXTRACT_USER.format(doc_id=chunk["doc_id"], path=chunk["path"], date=chunk["date"],
                                 chunk_id=chunk["chunk_id"], part=chunk["part"], parts=chunk["parts"],
                                 text=chunk["text"], feedback=feedback)
    try:
        result: ExtractionResult = call_structured("extract", ExtractionResult, P.EXTRACT_SYSTEM, user)
    except RuntimeError as exc:  # degrade gracefully: the completeness loop re-extracts what is missing
        log(f"extract[{chunk['chunk_id']}] round {rnd}: FAILED, continuing with no candidates ({exc})")
        result = ExtractionResult(requirements=[])
    candidates = []
    for i, r in enumerate(result.requirements, 1):
        c = r.model_dump()
        c.update(candidate_id=f"{chunk['chunk_id']}.r{rnd}.{i:02d}", doc_id=chunk["doc_id"],
                 chunk_id=chunk["chunk_id"], round=rnd, origin="extract",
                 grounded=is_grounded(r.quote, chunk["text"]))
        candidates.append(c)
    log(f"extract[{chunk['chunk_id']}] round {rnd}: {len(candidates)} candidates")
    return {"candidates": candidates}


# ---------------------------------------------------------------------------
# 3. collect_round (deterministic barrier: waits for all extract tasks, reports grounding)
# ---------------------------------------------------------------------------
def collect_round(state: dict) -> dict:
    rnd = state["extraction_round"]
    current = [c for c in state["candidates"] if c["round"] == rnd]
    ungrounded = sum(not c["grounded"] for c in current)
    log(f"collect_round {rnd}: {len(current)} new candidates ({ungrounded} with ungrounded quotes), "
        f"{len(state['candidates'])} total")
    return {"extraction_stats": state.get("extraction_stats", []) + [
        {"round": rnd, "chunks": len(state["active_chunks"]), "new_candidates": len(current),
         "ungrounded_quotes": ungrounded}]}


def fan_out_completeness(state: dict):
    chunks = {c["chunk_id"]: c for c in state["chunks"]}
    sends = []
    for cid in state["active_chunks"]:
        own = [c for c in state["candidates"] if c["chunk_id"] == cid]
        sends.append(Send("completeness_check", {"chunk": chunks[cid], "candidates": own,
                                                 "round": state["extraction_round"]}))
    return sends


# ---------------------------------------------------------------------------
# 4. completeness_check (LLM verifier of extract -> feedback loop 1)
# ---------------------------------------------------------------------------
def completeness_check(payload: dict) -> dict:
    chunk = payload["chunk"]
    extracted = "\n".join(f"- {c['statement']}" for c in payload["candidates"]) or "(nothing extracted)"
    user = P.COMPLETENESS_USER.format(chunk_id=chunk["chunk_id"], path=chunk["path"], text=chunk["text"],
                                      extracted=extracted)
    try:
        report: CompletenessReport = call_structured("completeness", CompletenessReport, P.COMPLETENESS_SYSTEM, user)
    except RuntimeError as exc:
        log(f"completeness_check[{chunk['chunk_id']}]: FAILED, treating chunk as checked ({exc})")
        report = CompletenessReport(complete=True, missed=[])
    missed = [m.model_dump() for m in report.missed]
    log(f"completeness_check[{chunk['chunk_id']}] round {payload['round']}: {len(missed)} missed")
    return {"coverage_reports": [{"chunk_id": chunk["chunk_id"], "round": payload["round"],
                                  "complete": report.complete and not missed, "missed": missed}]}


# ---------------------------------------------------------------------------
# 5. coverage_gate (deterministic decision of loop 1)
# ---------------------------------------------------------------------------
def coverage_gate(state: dict) -> dict:
    rnd = state["extraction_round"]
    gaps = [r for r in state["coverage_reports"] if r["round"] == rnd and r["missed"]]
    if gaps and rnd < MAX_EXTRACTION_ROUNDS:
        log(f"coverage_gate: {len(gaps)} chunks have gaps -> re-extraction round {rnd + 1}")
        return {"extraction_round": rnd + 1, "active_chunks": [g["chunk_id"] for g in gaps]}
    # Safety net (OS8): omissions still reported after the last round become candidates directly.
    chunks = {c["chunk_id"]: c for c in state["chunks"]}
    rescued = []
    for g in gaps:
        chunk = chunks[g["chunk_id"]]
        for i, m in enumerate(g["missed"], 1):
            rescued.append({
                "statement": m["description"], "quote": m["quote"], "category": "unspecified",
                "req_type": "functional", "priority_signal": "none", "stakeholder": "unknown",
                "suspicious": False, "suspicion_note": "", "candidate_id": f"{chunk['chunk_id']}.cc.{i:02d}",
                "doc_id": chunk["doc_id"], "chunk_id": chunk["chunk_id"], "round": rnd + 1,
                "origin": "completeness_check", "grounded": is_grounded(m["quote"], chunk["text"]),
            })
    log(f"coverage_gate: extraction finished ({len(rescued)} omissions added directly by the safety net)")
    return {"active_chunks": [], "candidates": rescued}


def route_after_coverage(state: dict):
    if not state["active_chunks"]:
        return "build_taxonomy"
    rnd = state["extraction_round"]
    chunks = {c["chunk_id"]: c for c in state["chunks"]}
    reports = {r["chunk_id"]: r for r in state["coverage_reports"] if r["round"] == rnd - 1}
    return [Send("extract", {
        "chunk": chunks[cid], "round": rnd, "missed": reports[cid]["missed"],
        "already": [c["statement"] for c in state["candidates"] if c["chunk_id"] == cid],
    }) for cid in state["active_chunks"]]


# ---------------------------------------------------------------------------
# 6. build_taxonomy (LLM: functional areas, glossary, candidate -> area)
# ---------------------------------------------------------------------------
def build_taxonomy(state: dict) -> dict:
    cands = state["candidates"]
    listing = "\n".join(f"- {c['candidate_id']} [{c['category']}] {c['statement']}" for c in cands)
    result: TaxonomyResult = call_structured("taxonomy", TaxonomyResult, P.TAXONOMY_SYSTEM,
                                             P.TAXONOMY_USER.format(n=len(cands), candidates=listing))
    areas, seen = [], set()
    for a in result.areas:
        code = re.sub(r"[^A-Z]", "", a.code.upper())[:4] or "GEN"
        while code in seen:
            code += "X"
        seen.add(code)
        areas.append({"code": code, "name": a.name, "description": a.description, "_orig": a.code})
    orig_to_code = {a["_orig"]: a["code"] for a in areas}
    names = {a["name"].lower(): a["code"] for a in areas}
    assignment = {}
    for asg in result.assignments:
        code = orig_to_code.get(asg.area_code) or (asg.area_code if asg.area_code in seen else None)
        if code:
            assignment[asg.candidate_id] = code
    # Deterministic repair: candidates the model forgot are assigned by their category hint.
    repaired = 0
    for c in cands:
        if c["candidate_id"] not in assignment:
            match = get_close_matches(c["category"].lower(), list(names), n=1, cutoff=0.0)
            assignment[c["candidate_id"]] = names[match[0]] if match else areas[0]["code"]
            repaired += 1
    for a in areas:
        a.pop("_orig")
    glossary = _sanitize_glossary([g.model_dump() for g in result.glossary])
    log(f"build_taxonomy: {len(areas)} areas, {len(glossary)} glossary terms, "
        f"{repaired} assignments repaired deterministically")
    return {"taxonomy": {"system_name": result.system_name, "system_summary": result.system_summary,
                         "areas": areas, "glossary": glossary, "assignment": assignment}}


_GENERIC_TERMS = {"system", "the system", "software", "application", "data", "information", "user interface"}


def _sanitize_glossary(glossary: list[dict]) -> list[dict]:
    """Drop synonyms that would cause false terminology findings: generic words, words that are part of the
    canonical term itself (e.g. 'query' for 'saved query'), and other canonical terms."""
    terms = {g["term"].lower() for g in glossary}
    for g in glossary:
        term_words = set(re.findall(r"\w+", g["term"].lower()))
        g["avoid"] = [s for s in g["avoid"]
                      if s.lower() not in _GENERIC_TERMS and s.lower() not in terms
                      and not set(re.findall(r"\w+", s.lower())) <= term_words]
    return glossary


def fan_out_consolidation(state: dict):
    tax = state["taxonomy"]
    sends = []
    for area in tax["areas"]:
        ids = [c["candidate_id"] for c in state["candidates"] if tax["assignment"][c["candidate_id"]] == area["code"]]
        if ids:
            sends.append(Send("consolidate", {"area": area, "candidate_ids": ids, "mode": "full",
                                              "previous": None, "missing": ids, **_shared(state)}))
    return sends or "validate"


def _shared(state: dict) -> dict:
    return {"documents": state["documents"], "candidates": state["candidates"], "taxonomy": state["taxonomy"]}


# ---------------------------------------------------------------------------
# 7. consolidate (LLM, one task per area; full mode or patch mode in loop 2)
# ---------------------------------------------------------------------------
def consolidate(payload: dict) -> dict:
    area, mode = payload["area"], payload["mode"]
    docs_by_id = {d["doc_id"]: d for d in payload["documents"]}
    cand_by_id = {c["candidate_id"]: c for c in payload["candidates"]}
    missing = payload["missing"]
    common = dict(area_code=area["code"], area_name=area["name"], area_description=area["description"],
                  glossary=_glossary_text(payload["taxonomy"]), documents=_doc_register(payload["documents"]),
                  candidates="\n".join(_candidate_block(cand_by_id[c], docs_by_id) for c in missing))
    if mode == "full":
        user = P.CONSOLIDATE_USER.format(n=len(missing), **common)
    else:
        existing = "\n".join(f"- {r['id']} | {r['name']}: {r['description']}" for r in payload["previous"]["requirements"])
        user = P.CONSOLIDATE_PATCH_USER.format(existing=existing, **common)
    result: ConsolidationResult = call_structured("consolidate", ConsolidationResult, P.CONSOLIDATE_SYSTEM, user)

    allowed = set(missing)
    prev = payload["previous"] or {"requirements": [], "discarded": [], "candidate_ids": payload["candidate_ids"]}
    reqs = [dict(r) for r in prev["requirements"]]
    by_id = {r["id"]: r for r in reqs if r.get("id")}
    for r in result.requirements:
        srcs = [c for c in r.source_candidates if c in allowed]  # drop hallucinated ids
        data = r.model_dump()
        if mode == "patch" and r.id in by_id:
            target = by_id[r.id]
            target["source_candidates"] = sorted(set(target["source_candidates"]) | set(srcs))
            for k in ("name", "description", "req_type", "priority", "priority_rationale"):
                target[k] = data[k]
        elif srcs:
            data.update(id=None, area=area["code"], source_candidates=srcs)
            reqs.append(data)
    discarded = list(prev["discarded"])
    for d in result.discarded:
        ids = [c for c in d.candidate_ids if c in allowed]
        if ids:
            discarded.append({**d.model_dump(), "candidate_ids": ids, "area": area["code"]})
    log(f"consolidate[{area['code']}] {mode}: {len(missing)} candidates -> {len(reqs)} requirements, "
        f"{len(discarded)} discarded")
    return {"area_results": {area["code"]: {"requirements": reqs, "discarded": discarded,
                                            "candidate_ids": prev["candidate_ids"]}}}


# ---------------------------------------------------------------------------
# 8. validate (deterministic: IDs, coverage of every candidate -> loop 2, lint)
# ---------------------------------------------------------------------------
def lint(requirements: list[dict], taxonomy: dict) -> list[dict]:
    """Deterministic quality checks for OS2, OS4, OS5, OS6, OS7."""
    issues = []
    names: dict[str, str] = {}
    synonyms = [(s, g["term"]) for g in taxonomy["glossary"] for s in g["avoid"]
                if s and s.lower() != g["term"].lower()]
    for r in requirements:
        rid = r["id"]
        if len(r["description"].split()) < MIN_DESCRIPTION_WORDS:
            issues.append({"issue_type": "format", "requirement_ids": [rid],
                           "description": f"Description shorter than {MIN_DESCRIPTION_WORDS} words.",
                           "suggested_fix": "Expand to a full paragraph with scope and details."})
        if len(r["name"].split()) > MAX_NAME_WORDS:
            issues.append({"issue_type": "format", "requirement_ids": [rid],
                           "description": f"Name longer than {MAX_NAME_WORDS} words.",
                           "suggested_fix": "Shorten the name."})
        if not r["description"].lstrip().lower().startswith("the system shall"):
            issues.append({"issue_type": "format", "requirement_ids": [rid],
                           "description": "Description does not start with 'The system shall'.",
                           "suggested_fix": "Rephrase the first sentence as 'The system shall ...'."})
        if r["priority"] not in PRIORITY_LEVELS:
            issues.append({"issue_type": "priority", "requirement_ids": [rid],
                           "description": f"Invalid priority {r['priority']}.", "suggested_fix": "Use P1-P4."})
        key = re.sub(r"\W+", " ", r["name"].lower()).strip()
        if key in names:
            issues.append({"issue_type": "duplicate", "requirement_ids": [names[key], rid],
                           "description": "Two requirements have the same name.",
                           "suggested_fix": "Merge them or make the names distinct."})
        names.setdefault(key, rid)
        text = f"{r['name']} {r['description']}"
        bad = sorted({f"'{s}' -> '{t}'" for s, t in synonyms if re.search(rf"\b{re.escape(s)}\b", text, re.I)})
        if bad:
            issues.append({"issue_type": "terminology", "requirement_ids": [rid],
                           "description": f"Uses non-canonical terms: {', '.join(bad)}.",
                           "suggested_fix": "Replace with the canonical glossary terms."})
    return issues


def validate(state: dict) -> dict:
    results = {code: {**res, "requirements": [dict(r) for r in res["requirements"]]}
               for code, res in state["area_results"].items()}
    # Stable unique IDs (OS2): REQ-<AREA>-<NNN>, never reused.
    for code, res in results.items():
        used = [int(r["id"].rsplit("-", 1)[1]) for r in res["requirements"] if r.get("id")]
        nxt = max(used, default=0) + 1
        for r in res["requirements"]:
            if not r.get("id"):
                r["id"] = f"REQ-{code}-{nxt:03d}"
                nxt += 1
    # Coverage (OS8): every candidate must be in a requirement or discarded.
    unaccounted = {}
    for code, res in results.items():
        accounted = {c for r in res["requirements"] for c in r["source_candidates"]}
        accounted |= {c for d in res["discarded"] for c in d["candidate_ids"]}
        missing = [c for c in res["candidate_ids"] if c not in accounted]
        if missing:
            unaccounted[code] = missing
    rnd = state["consolidation_round"]
    n_missing = sum(map(len, unaccounted.values()))
    if unaccounted and rnd < MAX_CONSOLIDATION_ROUNDS:
        log(f"validate: {n_missing} unaccounted candidates in {len(unaccounted)} areas -> patch round {rnd + 1}")
        return {"area_results": results, "unaccounted": unaccounted, "consolidation_round": rnd + 1}

    cand_by_id = {c["candidate_id"]: c for c in state["candidates"]}
    order = [a["code"] for a in state["taxonomy"]["areas"]]
    requirements, blacklist = [], []
    for code in order:
        if code not in results:
            continue
        for r in results[code]["requirements"]:
            requirements.append({**r, "area": code, "sources": _sources_of(r["source_candidates"], cand_by_id),
                                 "merged_from": []})
        for d in results[code]["discarded"]:
            blacklist.append({**d, "sources": _sources_of(d["candidate_ids"], cand_by_id), "stage": "consolidation"})
    unresolved = [c for ids in unaccounted.values() for c in ids]
    lint_issues = lint(requirements, state["taxonomy"])
    log(f"validate: {len(requirements)} requirements, {len(blacklist)} discarded, {len(unresolved)} unresolved, "
        f"{len(lint_issues)} lint issues")
    return {"area_results": results, "unaccounted": {}, "requirements": requirements, "blacklist": blacklist,
            "unresolved": unresolved, "lint_issues": lint_issues}


def route_after_validate(state: dict):
    if not state["unaccounted"]:
        return "review"
    return [Send("consolidate", {"area": next(a for a in state["taxonomy"]["areas"] if a["code"] == code),
                                 "candidate_ids": state["area_results"][code]["candidate_ids"], "mode": "patch",
                                 "previous": state["area_results"][code], "missing": ids, **_shared(state)})
            for code, ids in state["unaccounted"].items()]


# ---------------------------------------------------------------------------
# 9. review (LLM critic over the whole set -> loop 3)
# ---------------------------------------------------------------------------
def review(state: dict) -> dict:
    reqs, rnd = state["requirements"], state["review_round"]
    lint_issues = lint(reqs, state["taxonomy"])
    lint_text = "\n".join(f"- {i['issue_type']} {i['requirement_ids']}: {i['description']}" for i in lint_issues) or "(none)"
    user = P.REVIEW_USER.format(glossary=_glossary_text(state["taxonomy"]), n=len(reqs),
                                requirements="\n".join(_req_line(r) for r in reqs), lint=lint_text)
    result: ReviewResult = call_structured("review", ReviewResult, P.REVIEW_SYSTEM, user)
    known = {r["id"] for r in reqs}
    issues = []
    for i in result.issues:
        ids = [x for x in i.requirement_ids if x in known]
        if ids:
            issues.append({**i.model_dump(), "requirement_ids": ids, "source": "llm"})
    llm_keys = {(tuple(sorted(i["requirement_ids"])), i["issue_type"]) for i in issues}
    issues += [{**i, "source": "lint"} for i in lint_issues
               if (tuple(sorted(i["requirement_ids"])), i["issue_type"]) not in llm_keys]
    approved = not issues
    log(f"review round {rnd}: {len(issues)} issues ({len(lint_issues)} from lint), approved={approved}")
    return {"pending_issues": issues, "lint_issues": lint_issues,
            "review_history": [{"round": rnd, "approved": approved, "summary": result.summary,
                                "issues": issues}]}


def route_after_review(state: dict):
    if state["pending_issues"] and state["review_round"] < MAX_REVIEW_ROUNDS:
        return "revise"
    return "render"


# ---------------------------------------------------------------------------
# 10. revise (LLM proposes edits, applied deterministically)
# ---------------------------------------------------------------------------
def revise(state: dict) -> dict:
    issues = state["pending_issues"]
    reqs = {r["id"]: dict(r) for r in state["requirements"]}
    affected = sorted({rid for i in issues for rid in i["requirement_ids"]})
    user = P.REVISE_USER.format(
        glossary=_glossary_text(state["taxonomy"]),
        issues="\n".join(f"- [{i['issue_type']}] {', '.join(i['requirement_ids'])}: {i['description']} "
                         f"Suggested fix: {i['suggested_fix']}" for i in issues),
        requirements="\n".join(_req_line(reqs[rid]) for rid in affected),
    )
    result: RevisionResult = call_structured("revise", RevisionResult, P.REVISE_SYSTEM, user)
    cand_by_id = {c["candidate_id"]: c for c in state["candidates"]}
    blacklist = list(state["blacklist"])
    n_merge = n_update = n_remove = 0
    for m in result.merges:
        if m.keep_id not in reqs:
            continue
        keep = reqs[m.keep_id]
        for aid in m.absorb_ids:
            if aid == m.keep_id or aid not in reqs:
                continue
            absorbed = reqs.pop(aid)
            keep["source_candidates"] = sorted(set(keep["source_candidates"]) | set(absorbed["source_candidates"]))
            keep["merged_from"] = keep.get("merged_from", []) + [aid] + absorbed.get("merged_from", [])
            n_merge += 1
        keep.update(name=m.name, description=m.description, priority=m.priority,
                    priority_rationale=m.priority_rationale,
                    sources=_sources_of(keep["source_candidates"], cand_by_id))
    for u in result.updates:
        if u.id in reqs:
            reqs[u.id].update(name=u.name, description=u.description, req_type=u.req_type,
                              priority=u.priority, priority_rationale=u.priority_rationale)
            n_update += 1
    for rm in result.removals:
        if rm.id not in reqs:
            continue
        r = reqs.pop(rm.id)
        blacklist.append({"candidate_ids": r["source_candidates"], "statement": f"{r['name']}: {r['description']}",
                          "reason_category": rm.reason_category, "explanation": rm.explanation,
                          "related_requirement": rm.related_requirement, "area": r["area"],
                          "sources": r["sources"], "stage": f"review round {state['review_round']}",
                          "former_id": rm.id})
        n_remove += 1
    order = [r["id"] for r in state["requirements"] if r["id"] in reqs]
    log(f"revise round {state['review_round']}: {n_merge} merged, {n_update} updated, {n_remove} removed")
    return {"requirements": [reqs[i] for i in order], "blacklist": blacklist,
            "review_round": state["review_round"] + 1,
            "revision_log": [{"round": state["review_round"], "merged": n_merge, "updated": n_update,
                              "removed": n_remove, "notes": result.notes}]}


# ---------------------------------------------------------------------------
# 11. render (deterministic: Markdown + JSON)
# ---------------------------------------------------------------------------
def render(state: dict) -> dict:
    outputs = render_outputs(state)
    log(f"render: wrote {', '.join(outputs.values())}")
    return {"outputs": outputs}
