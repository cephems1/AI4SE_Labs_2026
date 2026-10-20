"""Deterministic rendering of the final requirements document (Markdown) and its JSON twin."""

import json
from datetime import date
from pathlib import Path

from .config import DISCARD_CATEGORIES, PRIORITY_SCALE, model_for
from .llm import usage_report

_PRIO_LABEL = {p["level"]: p["label"] for p in PRIORITY_SCALE}


def _cell(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def _resolve_related(text: str, requirements: list[dict]) -> str:
    """Map a free-text reference (name or id) to a requirement id where possible."""
    if not text:
        return ""
    ids = {r["id"] for r in requirements}
    found = [i for i in ids if i in text]
    if found:
        return ", ".join(sorted(found))
    by_name = {r["name"].lower(): r["id"] for r in requirements}
    rid = by_name.get(text.strip().lower())
    return f"{rid} ({text})" if rid else text


def render_outputs(state: dict) -> dict:
    out_dir = Path(state["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    tax = state["taxonomy"]
    docs = state["documents"]
    reqs = state["requirements"]
    cand_by_id = {c["candidate_id"]: c for c in state["candidates"]}
    areas = {a["code"]: a for a in tax["areas"]}
    for i, b in enumerate(state["blacklist"], 1):
        b["id"] = f"BL-{i:03d}"

    trace = {d["doc_id"]: [] for d in docs}
    for r in reqs:
        for s in r["sources"]:
            trace[s].append(r["id"])

    L = []
    L += [f"# {tax['system_name']} - Software Requirements Specification", "",
          f"*Generated on {date.today().isoformat()} by the LangGraph requirements-refinement network "
          f"from {len(docs)} input documents.*", ""]

    # 1. Introduction
    by_prio = {p: sum(r["priority"] == p for r in reqs) for p in _PRIO_LABEL}
    L += ["## 1. Introduction", "", tax["system_summary"], "",
          f"This document consolidates **{len(reqs)} requirements** "
          f"({', '.join(f'{n} × {p}' for p, n in by_prio.items())}) derived from "
          f"**{len(state['candidates'])} candidate statements** extracted from the corpus. Semantically duplicate "
          f"statements were merged; **{len(state['blacklist'])} statements were discarded** and are listed with "
          f"reasons in Section 8. Every requirement has a unique identifier `REQ-<AREA>-<NNN>` and lists the input "
          f"documents it was derived from (Sections 6 and 7).", ""]

    # 2. Source documents
    L += ["## 2. Source Documents", "", "| Doc ID | File | Date | Requirements traced |", "|---|---|---|---|"]
    L += [f"| {d['doc_id']} | `{d['path']}` | {d['date']} | {len(trace[d['doc_id']])} |" for d in docs]
    L.append("")

    # 3. Priority scale
    L += ["## 3. Priority Scale", "", "| Priority | Label | Meaning | Assigned when |", "|---|---|---|---|"]
    L += [f"| **{p['level']}** | {p['label']} | {p['meaning']} | {p['criteria']} |" for p in PRIORITY_SCALE]
    L.append("")

    # 4. Glossary
    L += ["## 4. Glossary", "", "All requirements use the canonical terms below; the listed synonyms found in the "
          "source documents were normalised to them.", "", "| Term | Definition | Replaces |", "|---|---|---|"]
    L += [f"| **{_cell(g['term'])}** | {_cell(g['definition'])} | {_cell(', '.join(g['avoid']))} |"
          for g in tax["glossary"]]
    L.append("")

    # 5. Overview
    L += ["## 5. Requirements Overview", ""]
    L += [f"| Area | Name | Requirements |", "|---|---|---|"]
    L += [f"| {a['code']} | {a['name']} | {sum(r['area'] == a['code'] for r in reqs)} |" for a in tax["areas"]]
    L += ["", "| ID | Name | Priority | Type |", "|---|---|---|---|"]
    L += [f"| [{r['id']}](#{r['id'].lower()}) | {_cell(r['name'])} | {r['priority']} | {r['req_type']} |" for r in reqs]
    L.append("")

    # 6. Detailed requirements
    L += ["## 6. Detailed Requirements", ""]
    doc_by_id = {d["doc_id"]: d for d in docs}
    for code, area in areas.items():
        area_reqs = [r for r in reqs if r["area"] == code]
        if not area_reqs:
            continue
        L += [f"### 6.{list(areas).index(code) + 1} {area['name']} ({code})", "", area["description"], ""]
        for r in area_reqs:
            srcs = ", ".join(f"{s} (`{doc_by_id[s]['path']}`)" for s in r["sources"])
            L += [f'<a id="{r["id"].lower()}"></a>', f"#### {r['id']}: {r['name']}", "",
                  f"- **Priority:** {r['priority']} ({_PRIO_LABEL.get(r['priority'], '?')}) - {r['priority_rationale']}",
                  f"- **Type:** {r['req_type']}",
                  f"- **Derived from:** {srcs}"]
            if r.get("merged_from"):
                L.append(f"- **Merged with:** {', '.join(r['merged_from'])} (during review)")
            L += ["", r["description"], ""]
            evidence = [cand_by_id[c] for c in r["source_candidates"] if c in cand_by_id]
            L += [f"<details><summary>Evidence ({len(evidence)} source statements)</summary>", ""]
            L += [f"- {c['doc_id']}: \"{_cell(c['quote'])}\"" for c in evidence]
            L += ["", "</details>", ""]

    # 7. Traceability matrix
    L += ["## 7. Traceability Matrix", "", "| Doc ID | File | Requirements |", "|---|---|---|"]
    L += [f"| {d['doc_id']} | `{d['path']}` | {', '.join(trace[d['doc_id']]) or '-'} |" for d in docs]
    L.append("")

    # 8. Blacklist
    L += ["## 8. Discarded Requirements (Blacklist)", "",
          "Statements identified as requirements in the input documents but not included in the specification.",
          "", "| Category | Meaning |", "|---|---|"]
    L += [f"| {k} | {v} |" for k, v in DISCARD_CATEGORIES.items()]
    L += ["", "| ID | Discarded statement | Category | Explanation | Related requirement | Sources |",
          "|---|---|---|---|---|---|"]
    for b in state["blacklist"]:
        L.append(f"| {b['id']} | {_cell(b['statement'])} | {b['reason_category']} | {_cell(b['explanation'])} | "
                 f"{_cell(_resolve_related(b['related_requirement'], reqs)) or '-'} | {', '.join(b['sources'])} |")
    L.append("")

    # 9. Manual review
    if state.get("unresolved"):
        L += ["## 9. Statements Requiring Manual Review", "",
              "These extracted statements could not be consolidated automatically within the iteration limit.", ""]
        L += [f"- {cand_by_id[c]['doc_id']}: {cand_by_id[c]['statement']}" for c in state["unresolved"]]
        L.append("")

    # Appendix
    last = state["review_history"][-1] if state.get("review_history") else None
    L += ["## Appendix A. Generation Report", "", "| Role | Model | Calls | Input tokens | Output tokens |",
          "|---|---|---|---|---|"]
    usage = usage_report()
    L += [f"| {role} | {u['model']} | {u['calls']} | {u['input_tokens']} | {u['output_tokens']} |"
          for role, u in usage.items()]
    L += ["", f"- Extraction rounds: {len(state.get('extraction_stats', []))}, consolidation patch rounds: "
          f"{state.get('consolidation_round', 0)}, review rounds: {len(state.get('review_history', []))}"]
    for h in state.get("review_history", []):
        L.append(f"- Review round {h['round']}: {len(h['issues'])} issues, approved={h['approved']}. {h['summary']}")
    if last and last["issues"]:
        L += ["", "Open findings of the last review round (not fixed within the iteration limit):", ""]
        L += [f"- [{i['issue_type']}] {', '.join(i['requirement_ids'])}: {_cell(i['description'])}" for i in last["issues"]]
    L.append("")

    md_path = out_dir / "requirements.md"
    md_path.write_text("\n".join(L), encoding="utf-8")

    json_path = out_dir / "requirements.json"
    json_path.write_text(json.dumps({
        "system_name": tax["system_name"], "system_summary": tax["system_summary"],
        "priority_scale": PRIORITY_SCALE, "areas": tax["areas"], "glossary": tax["glossary"],
        "documents": [{k: d[k] for k in ("doc_id", "path", "date", "chars")} for d in docs],
        "requirements": reqs, "blacklist": state["blacklist"], "unresolved": state.get("unresolved", []),
        "candidates": state["candidates"],
        "run": {"models": {role: model_for(role) for role in usage} , "usage": usage,
                "extraction_stats": state.get("extraction_stats", []),
                "coverage_reports": state.get("coverage_reports", []),
                "review_history": state.get("review_history", []),
                "revision_log": state.get("revision_log", [])},
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"markdown": str(md_path), "json": str(json_path)}
