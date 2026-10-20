"""LangGraph wiring of the requirements-refinement network."""

import operator
from typing import Annotated, TypedDict

from langgraph.graph import END, START, StateGraph

from . import nodes as N


def _merge_dicts(left: dict | None, right: dict | None) -> dict:
    return {**(left or {}), **(right or {})}


class State(TypedDict, total=False):
    input_dir: str
    output_dir: str
    documents: list[dict]
    chunks: list[dict]
    # loop 1: extraction <-> completeness check
    candidates: Annotated[list[dict], operator.add]
    coverage_reports: Annotated[list[dict], operator.add]
    extraction_round: int
    active_chunks: list[str]
    extraction_stats: list[dict]
    # structure
    taxonomy: dict
    # loop 2: consolidation <-> coverage validation
    area_results: Annotated[dict, _merge_dicts]
    consolidation_round: int
    unaccounted: dict
    unresolved: list[str]
    # loop 3: review <-> revise
    requirements: list[dict]
    blacklist: list[dict]
    lint_issues: list[dict]
    pending_issues: list[dict]
    review_round: int
    review_history: Annotated[list[dict], operator.add]
    revision_log: Annotated[list[dict], operator.add]
    outputs: dict


def build_graph():
    g = StateGraph(State)
    g.add_node("load_corpus", N.load_corpus)              # deterministic
    g.add_node("extract", N.extract)                      # LLM
    g.add_node("collect_round", N.collect_round)          # deterministic barrier
    g.add_node("completeness_check", N.completeness_check)  # LLM verifier
    g.add_node("coverage_gate", N.coverage_gate)          # deterministic
    g.add_node("build_taxonomy", N.build_taxonomy)        # LLM
    g.add_node("consolidate", N.consolidate)              # LLM
    g.add_node("validate", N.validate)                    # deterministic verifier
    g.add_node("review", N.review)                        # LLM critic (+ deterministic lint)
    g.add_node("revise", N.revise)                        # LLM
    g.add_node("render", N.render)                        # deterministic

    g.add_edge(START, "load_corpus")
    g.add_conditional_edges("load_corpus", N.fan_out_extraction, ["extract"])
    g.add_edge("extract", "collect_round")
    g.add_conditional_edges("collect_round", N.fan_out_completeness, ["completeness_check"])
    g.add_edge("completeness_check", "coverage_gate")
    g.add_conditional_edges("coverage_gate", N.route_after_coverage, ["extract", "build_taxonomy"])
    g.add_conditional_edges("build_taxonomy", N.fan_out_consolidation, ["consolidate", "validate"])
    g.add_edge("consolidate", "validate")
    g.add_conditional_edges("validate", N.route_after_validate, ["consolidate", "review"])
    g.add_conditional_edges("review", N.route_after_review, ["revise", "render"])
    g.add_edge("revise", "review")
    g.add_edge("render", END)
    return g.compile()
