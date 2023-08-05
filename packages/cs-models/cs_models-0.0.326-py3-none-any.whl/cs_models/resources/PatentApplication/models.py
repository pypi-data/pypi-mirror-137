from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
)
from datetime import datetime

from ...database import Base


class PatentApplicationModel(Base):
    __tablename__ = 'patent_applications'

    id = Column(Integer, primary_key=True)
    application_number = Column(String(128), nullable=False)
    jurisdiction = Column(String(128), nullable=False)
    abstract_text = Column(Text)
    filed_date = Column(DateTime)
    inventors = Column(Text)
    title = Column(String(500))

    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    __table_args__ = (UniqueConstraint('application_number', 'jurisdiction'),)
