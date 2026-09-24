from langchain_openai import ChatOpenAI
from pydantic import BaseModel,Field
from typing import Literal

class Issue(BaseModel):
    category: Literal[
        "BUG",
        "SECURITY",
        "QUALITY",
        "PERFORMANCE"
    ]

    severity: Literal[
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    ]

    file: str
    line: int | None = None
    description: str
    evidence: str
    recommendation: str


class CodeReview(BaseModel):
    summary: str
    overall_severity: Literal[
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "LOW"
    ]
    issues: list[Issue]
    testing_recommendations: list[str] = Field(default_factory= list)





