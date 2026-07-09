from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hcp_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specialty: Mapped[str | None] = mapped_column(String(255), nullable=True)
    institution: Mapped[str | None] = mapped_column(String(255), nullable=True)
    interaction_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    interaction_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    product_discussed: Mapped[str | None] = mapped_column(String(255), nullable=True)
    discussion_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    sentiment: Mapped[str | None] = mapped_column(String(50), nullable=True)
    key_topics: Mapped[list[str]] = mapped_column(JSON, default=list)
    materials_shared: Mapped[list[str]] = mapped_column(JSON, default=list)
    follow_up_required: Mapped[bool] = mapped_column(Boolean, default=False)
    follow_up_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    compliance_flags: Mapped[list[str]] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(50), default="Draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
