"""Models for representing QA reports."""
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError, validator, constr, Json


class Flag(BaseModel):
    id: str
    description: Optional[str]


class BaseReport(BaseModel):
    name: str = Field(title="Report Name", description="The full name of the report")
    key_name: str = Field(
        title="Report Key Name",
        description="The abbreviated name of the report",
        examples=["arxiv-example-report"],
        regex="^[a-z0-9]+(-[a-z0-9]+)*$",
    )
    version: str
    submission_id: int
    created: str = Field(default_factory=datetime.now(timezone.utc).isoformat)


class Report(BaseReport):
    flags: List[Flag] = []
    qa_exec_time_sec: Optional[int] = Field(
        description="Time it took to complete the QA check(s) for this report, in seconds.",
        ge=0,
    )
    data: dict


class TEIAnalysisReport(Report):
    name = "arXiv TEI Analysis"
    key_name: str = "tei-analysis"


class KeywordSearchReport(Report):
    name = "arXiv Fulltext Keyword Search Report"
    key_name: str = "fulltext-keywords"


class AuthorCheckReport(Report):
    name = "arXiv Author Metadata Report"
    key_name: str = "author-check"


class FulltextReport(Report):
    name = "arXiv Fulltext Report"
    key_name: str = "fulltext"


class OverlapReport(Report):
    name = "arXiv Overlap Report"
    key_name: str = "overlap"


class PDFInfoReport(Report):
    name = "arXiv PDFInfo Report"
    key_name: str = "pdfinfo"


class TeXWrappedReport(Report):
    name = "arXiv TeX Wrapped Report"
    key_name: str = "tex-wrapped"


class TeXCreatedReport(Report):
    name = "arXiv TeX Created Report"
    key_name: str = "tex-created"


class SummaryReport(BaseReport):
    name = "arXiv Submission QA Summary Report"
    key_name: str = "qa-summary"
    version = "1.0"
    reports: List[Report] = []
    flagged_report_keys: Optional[List[str]] = []
    missing_report_keys: Optional[List[str]] = []

    @validator("flagged_report_keys")
    def flagged_report_keys_match_reports(cls, v, values):
        if len(v) > 0:
            for report_key in v:
                found_report_key = False
                for report in values["reports"]:
                    if report_key == report.key_name:
                        found_report_key = True
                        if len(report.flags) == 0:
                            raise ValueError(
                                "expect at find least 1 flag in flagged report"
                            )
                        continue
                if not found_report_key:
                    raise ValueError("report key not found in reports")


class SubmissionQAReport(BaseModel):
    id: int
    submission_id: int
    report_key_name: constr(max_length=64)
    created: Optional[datetime]
    num_flags: int
    report: Json
    # report: Report = Field(default_factory=Report)
    report_uri: constr(max_length=256) = None

    class Config:
        orm_mode = True
