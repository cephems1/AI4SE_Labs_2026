"""Pydantic schemas for structured LLM outputs.

All fields are required (no defaults) so that OpenAI strict JSON-schema mode can be used.
Optional values are expressed as nullable types or empty strings/lists.
"""

from typing import Literal, Optional

from pydantic import BaseModel, Field

ReqType = Literal["functional", "non-functional", "constraint"]
Priority = Literal["P1", "P2", "P3", "P4"]
DiscardCategory = Literal["conflict", "superseded", "nonsensical", "out_of_scope", "not_a_requirement"]


# ---------- extract ----------
class ExtractedRequirement(BaseModel):
    statement: str = Field(description="One atomic, testable requirement written as 'The system shall ...'.")
    quote: str = Field(description="Shortest verbatim excerpt from the text that supports the requirement (max ~300 chars).")
    category: str = Field(description="Short functional-area hint, e.g. 'Reporting', 'Security', 'Inventory'.")
    req_type: ReqType
    priority_signal: str = Field(description="Explicit priority evidence copied from the text, or 'none'.")
    stakeholder: str = Field(description="Who expressed the need (name/role), or 'unknown'.")
    suspicious: bool = Field(description="True if the requirement looks nonsensical, infeasible, a joke, or contradictory.")
    suspicion_note: str = Field(description="Why it is suspicious; empty string if not suspicious.")


class ExtractionResult(BaseModel):
    requirements: list[ExtractedRequirement]


# ---------- completeness_check ----------
class MissedRequirement(BaseModel):
    description: str = Field(description="What requirement was missed.")
    quote: str = Field(description="Verbatim excerpt from the text where it is stated.")


class CompletenessReport(BaseModel):
    complete: bool = Field(description="True if the extracted list covers every requirement in the excerpt.")
    missed: list[MissedRequirement]


# ---------- build_taxonomy ----------
class Area(BaseModel):
    code: str = Field(description="2-4 uppercase letters, unique, e.g. 'RPT'.")
    name: str
    description: str


class GlossaryTerm(BaseModel):
    term: str = Field(description="Canonical term to use in all requirements.")
    definition: str
    avoid: list[str] = Field(description="Synonyms found in the corpus that must be replaced by the canonical term.")


class Assignment(BaseModel):
    candidate_id: str
    area_code: str


class TaxonomyResult(BaseModel):
    system_name: str
    system_summary: str = Field(description="One paragraph describing the system and its stakeholders.")
    areas: list[Area]
    glossary: list[GlossaryTerm]
    assignments: list[Assignment]


# ---------- consolidate ----------
class ConsolidatedRequirement(BaseModel):
    id: Optional[str] = Field(description="Existing requirement id when extending a previous requirement (patch mode); null for a new requirement.")
    name: str = Field(description="Short descriptive name, max 10 words, Title Case.")
    description: str = Field(description="One paragraph (3-6 sentences) starting with 'The system shall'.")
    req_type: ReqType
    priority: Priority
    priority_rationale: str = Field(description="One sentence justifying the priority with evidence from the candidates.")
    source_candidates: list[str] = Field(description="IDs of ALL candidates merged into this requirement.")


class Discard(BaseModel):
    candidate_ids: list[str]
    statement: str = Field(description="The discarded requirement as it was stated.")
    reason_category: DiscardCategory
    explanation: str = Field(description="Why it was discarded; for conflicts name the conflicting statement and why the other one won.")
    related_requirement: str = Field(description="Name or id of the kept requirement it conflicts with / is superseded by, or empty string.")


class ConsolidationResult(BaseModel):
    requirements: list[ConsolidatedRequirement]
    discarded: list[Discard]


# ---------- review ----------
class ReviewIssue(BaseModel):
    issue_type: Literal["duplicate", "conflict", "terminology", "vague", "priority", "format", "other"]
    requirement_ids: list[str]
    description: str
    suggested_fix: str


class ReviewResult(BaseModel):
    approved: bool = Field(description="True only if there are no issues worth fixing.")
    summary: str
    issues: list[ReviewIssue]


# ---------- revise ----------
class RequirementUpdate(BaseModel):
    id: str
    name: str
    description: str
    req_type: ReqType
    priority: Priority
    priority_rationale: str


class Merge(BaseModel):
    keep_id: str
    absorb_ids: list[str]
    name: str
    description: str
    priority: Priority
    priority_rationale: str


class Removal(BaseModel):
    id: str
    reason_category: DiscardCategory
    explanation: str
    related_requirement: str


class RevisionResult(BaseModel):
    updates: list[RequirementUpdate]
    merges: list[Merge]
    removals: list[Removal]
    notes: str
