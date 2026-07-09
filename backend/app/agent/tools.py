from typing import Any, Literal

from langchain_core.tools import tool
from pydantic import BaseModel, Field


Sentiment = Literal["Positive", "Neutral", "Negative", "Unknown"]
InteractionStatus = Literal["Draft", "Ready to Submit", "Submitted"]


class InteractionPatch(BaseModel):
    hcp_name: str | None = None
    specialty: str | None = None
    institution: str | None = None
    interaction_type: str | None = None
    interaction_date: str | None = None
    product_discussed: str | None = None
    discussion_summary: str | None = None
    sentiment: Sentiment | None = None
    key_topics: list[str] | None = None
    materials_shared: list[str] | None = None
    follow_up_required: bool | None = None
    follow_up_date: str | None = None
    compliance_flags: list[str] | None = None
    status: InteractionStatus | None = None


class LogInteractionInput(BaseModel):
    patch: InteractionPatch = Field(
        ...,
        description="Structured fields extracted from the representative's natural-language note.",
    )


class EditInteractionInput(BaseModel):
    field: str = Field(..., description="The snake_case form field to update.")
    value: Any = Field(..., description="The new value for the selected field.")


class ComplianceInput(BaseModel):
    discussion_summary: str = Field(
        ...,
        description="Interaction summary or raw note to check for life-sciences compliance risk.",
    )
    product_discussed: str | None = Field(
        default=None,
        description="The product mentioned in the interaction, if known.",
    )


class FollowUpInput(BaseModel):
    sentiment: Sentiment = Field(..., description="The HCP sentiment after the interaction.")
    key_topics: list[str] = Field(default_factory=list)
    requested_materials: list[str] = Field(default_factory=list)


class SummaryInput(BaseModel):
    raw_notes: str = Field(..., description="Rough notes from the field representative.")


@tool(args_schema=LogInteractionInput)
def log_interaction_tool(patch: InteractionPatch) -> dict[str, Any]:
    """Fill the HCP interaction form from a natural-language interaction note."""
    return {
        "form_patch": patch.model_dump(exclude_none=True),
        "assistant_message": "I updated the interaction form from your note.",
    }


@tool(args_schema=EditInteractionInput)
def edit_interaction_tool(field: str, value: Any) -> dict[str, Any]:
    """Update one specific interaction form field after the user gives a correction."""
    return {
        "form_patch": {field: value},
        "assistant_message": f"I updated {field}.",
    }


@tool(args_schema=ComplianceInput)
def validate_compliance_tool(
    discussion_summary: str,
    product_discussed: str | None = None,
) -> dict[str, Any]:
    """Check an HCP interaction note for common regulated life-sciences compliance risks."""
    flags: list[str] = []
    summary_lower = discussion_summary.lower()

    risk_terms = {
        "off-label": "Possible off-label discussion",
        "guarantee": "Possible guarantee or overstatement",
        "cash": "Possible inducement concern",
        "gift": "Possible gift or inducement concern",
        "adverse event": "Possible adverse event mention",
        "side effect": "Possible adverse event mention",
    }

    for term, flag in risk_terms.items():
        if term in summary_lower and flag not in flags:
            flags.append(flag)

    if product_discussed and product_discussed.lower() not in summary_lower:
        flags.append("Product is listed but not clearly reflected in the summary")

    return {
        "compliance_flags": flags,
        "assistant_message": (
            "I found compliance items to review." if flags else "No obvious compliance risks found."
        ),
        "form_patch": {"compliance_flags": flags},
    }


@tool(args_schema=FollowUpInput)
def suggest_followup_tool(
    sentiment: Sentiment,
    key_topics: list[str],
    requested_materials: list[str],
) -> dict[str, Any]:
    """Suggest follow-up actions based on HCP sentiment, key topics, and requested materials."""
    follow_up_required = sentiment in ["Positive", "Neutral"] or bool(requested_materials)
    topics_text = ", ".join(key_topics) if key_topics else "the discussed topics"

    if requested_materials:
        action = f"Send approved materials for {', '.join(requested_materials)}."
    elif sentiment == "Negative":
        action = f"Plan a careful follow-up to understand concerns around {topics_text}."
    else:
        action = f"Follow up with approved information about {topics_text}."

    return {
        "assistant_message": action,
        "form_patch": {
            "follow_up_required": follow_up_required,
            "status": "Draft",
        },
        "recommended_action": action,
    }


@tool(args_schema=SummaryInput)
def summarize_interaction_tool(raw_notes: str) -> dict[str, Any]:
    """Turn rough representative notes into a concise CRM-ready interaction summary."""
    cleaned_notes = " ".join(raw_notes.split())
    if len(cleaned_notes) > 450:
        cleaned_notes = cleaned_notes[:447].rstrip() + "..."

    return {
        "assistant_message": "I prepared a concise CRM summary.",
        "form_patch": {"discussion_summary": cleaned_notes},
    }


CRM_TOOLS = [
    log_interaction_tool,
    edit_interaction_tool,
    validate_compliance_tool,
    suggest_followup_tool,
    summarize_interaction_tool,
]

