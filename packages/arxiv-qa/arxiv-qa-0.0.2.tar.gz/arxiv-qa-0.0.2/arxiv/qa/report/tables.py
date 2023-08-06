"""QA table definitions."""

from sqlalchemy import Column, DateTime, ForeignKey, JSON, String, text
from sqlalchemy.dialects.mysql import (
    INTEGER,
    SMALLINT,
)

# from sqlalchemy.orm import relationships
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DBSubmissionQAReport(Base):
    __tablename__ = "arXiv_submission_qa_reports"

    id = Column(INTEGER(11), primary_key=True)
    submission_id = Column(
        ForeignKey("arXiv_submissions.submission_id"), nullable=False, index=True
    )
    report_key_name = Column(String(64), nullable=False, index=True)
    created = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    num_flags = Column(SMALLINT(6), nullable=False, server_default=text("'0'"))
    report = Column(JSON, nullable=False)
    report_uri = Column(String(256))

    # submission = relationship('ArXivSubmission')
