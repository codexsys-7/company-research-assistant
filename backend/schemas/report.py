from pydantic import BaseModel, Field, field_validator
from typing import List

_SENTINEL = "information not available"


def _filter_sentinels(items: list) -> list:
    """Remove placeholder 'Information not available' strings from list fields."""
    return [item for item in items if item.lower().strip() != _SENTINEL]


class CompanyReport(BaseModel):
    """Structured research report generated for a company prior to an interview."""

    company_name: str = Field(
        ...,
        description="The full legal or commonly known name of the company being researched.",
    )

    overview: str = Field(
        ...,
        description=(
            "A concise company overview covering founding history, mission, business model, "
            "industry, and current scale (headcount, geography, or revenue where available)."
        ),
    )

    products_and_services: str = Field(
        ...,
        description=(
            "Description of the company's core products and/or services, including key features, "
            "target customers, and how they differentiate in the market."
        ),
    )

    tech_stack: List[str] = Field(
        default_factory=list,
        description=(
            "List of technologies, languages, frameworks, and tools the company is known to use "
            "(e.g. ['Python', 'React', 'Kubernetes', 'PostgreSQL'])."
        ),
    )

    culture_and_values: str = Field(
        ...,
        description=(
            "Summary of the company's stated and observed culture, core values, work environment, "
            "diversity initiatives, and employee sentiment where available."
        ),
    )

    recent_news: List[str] = Field(
        default_factory=list,
        description=(
            "List of recent notable news headlines or events about the company "
            "(e.g. funding rounds, product launches, leadership changes, controversies)."
        ),
    )

    financials: str = Field(
        ...,
        description=(
            "Summary of publicly available financial information such as funding stage, valuation, "
            "revenue estimates, profitability, or stock performance. Use 'Not publicly available' if unknown."
        ),
    )

    interview_process: str = Field(
        ...,
        description=(
            "Description of the company's typical hiring process, including number of rounds, "
            "interview formats (technical, behavioural, case study), and approximate timeline."
        ),
    )

    common_interview_questions: List[str] = Field(
        default_factory=list,
        description=(
            "List of commonly reported interview questions for this company, sourced from candidate "
            "reviews and job forums (e.g. Glassdoor, Blind, Reddit)."
        ),
    )

    red_flags: List[str] = Field(
        default_factory=list,
        description=(
            "List of potential concerns or red flags identified from employee reviews, news, or public "
            "perception (e.g. high turnover, layoffs, culture issues, legal disputes)."
        ),
    )

    preparation_tips: str = Field(
        ...,
        description=(
            "Actionable advice for a candidate preparing to interview at this company, including topics "
            "to study, projects to highlight, and company-specific talking points."
        ),
    )

    @field_validator("tech_stack", "red_flags", "common_interview_questions", mode="before")
    @classmethod
    def filter_sentinel_strings(cls, v):
        if isinstance(v, list):
            return _filter_sentinels(v)
        return v

    @field_validator("recent_news", mode="before")
    @classmethod
    def limit_and_filter_recent_news(cls, v):
        if isinstance(v, list):
            return _filter_sentinels(v)[:5]
        return v
