"""
Draft Output Pydantic Schema.
Mirrors contracts/ai-schemas/draft_output.json.
"""

from typing import List
from pydantic import BaseModel, Field, constr


class ClaimItem(BaseModel):
    fact_id: str = Field(description="Identifier of verified input fact")
    claim: str = Field(description="Exact statement asserting the verified fact")


class AIDraftOutput(BaseModel):
    subject: constr(max_length=80) = Field(
        description="Engaging subject line capped at 80 characters"
    )
    body: str = Field(
        description="Outreach email body strictly derived from verified facts"
    )
    personalization_summary: str = Field(
        description="Explanation of why message is relevant to the recipient"
    )
    claims_used: List[ClaimItem] = Field(
        default_factory=list,
        description="Every factual claim made in body must map to an input fact_id"
    )
    missing_information_warnings: List[str] = Field(
        default_factory=list,
        description="Explicit warnings for missing attributes (e.g. salary, tech stack)"
    )
    confidence_note: str = Field(
        description="Self-assessment note regarding factual grounding"
    )
