from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    current_form: dict[str, Any] = Field(default_factory=dict)


class ChatResponse(BaseModel):
    assistant_message: str
    form_patch: dict[str, Any] = Field(default_factory=dict)
    compliance_flags: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    service: str


class InteractionBase(BaseModel):
    hcp_name: str | None = None
    specialty: str | None = None
    institution: str | None = None
    interaction_type: str | None = None
    interaction_date: str | None = None
    product_discussed: str | None = None
    discussion_summary: str | None = None
    sentiment: str | None = None
    key_topics: list[str] = Field(default_factory=list)
    materials_shared: list[str] = Field(default_factory=list)
    follow_up_required: bool = False
    follow_up_date: str | None = None
    compliance_flags: list[str] = Field(default_factory=list)
    status: str = "Draft"


class InteractionCreate(InteractionBase):
    pass


class InteractionResponse(InteractionBase):
    id: int
    created_at: Any

    model_config = {"from_attributes": True}
