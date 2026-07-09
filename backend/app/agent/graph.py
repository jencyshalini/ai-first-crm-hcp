import json
import os
from typing import Annotated, Any, Literal, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages

from app.agent.tools import CRM_TOOLS


load_dotenv()


SYSTEM_PROMPT = """
You are an AI-first CRM assistant for life-sciences field representatives.

The user is not allowed to manually fill the HCP interaction form.
You must control the form by calling tools.

Use these rules:
- If the user gives visit or call notes, call log_interaction_tool.
- If the user asks to change or correct a field, call edit_interaction_tool.
- If the note mentions claims, product discussion, safety, side effects, gifts, cash,
  guarantees, or off-label use, call validate_compliance_tool.
- If the HCP asks for material, data, another meeting, or next steps, call suggest_followup_tool.
- If the user asks to clean up notes or make a CRM summary, call summarize_interaction_tool.
- Never invent clinical facts.
- Use snake_case field names in form patches.
- Keep the final assistant message short and clear.
"""


class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


def _get_llm_with_tools():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    model_name = os.getenv("GROQ_MODEL", "gemma2-9b-it")
    llm = ChatGroq(
        model=model_name,
        temperature=0,
        max_retries=2,
        api_key=api_key,
    )
    return llm.bind_tools(CRM_TOOLS)


def _call_model(state: AgentState) -> dict[str, list[AnyMessage]]:
    llm_with_tools = _get_llm_with_tools()
    if llm_with_tools is None:
        return {
            "messages": [
                AIMessage(
                    content=(
                        "Groq is not configured yet. Create a backend/.env file with "
                        "GROQ_API_KEY before testing the AI agent."
                    )
                )
            ]
        }

    response = llm_with_tools.invoke([SystemMessage(content=SYSTEM_PROMPT)] + state["messages"])
    return {"messages": [response]}


def _call_tools(state: AgentState) -> dict[str, list[ToolMessage]]:
    tool_messages: list[ToolMessage] = []
    tools_by_name = {tool.name: tool for tool in CRM_TOOLS}
    last_message = state["messages"][-1]

    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        tool_messages.append(
            ToolMessage(
                content=json.dumps(result),
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
            )
        )

    return {"messages": tool_messages}


def _should_continue(state: AgentState) -> Literal["tools", "__end__"]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("model", _call_model)
    graph.add_node("tools", _call_tools)
    graph.add_edge(START, "model")
    graph.add_conditional_edges("model", _should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "model")
    return graph.compile()


crm_agent = build_graph()


def _merge_tool_outputs(messages: list[AnyMessage]) -> dict[str, Any]:
    form_patch: dict[str, Any] = {}
    compliance_flags: list[str] = []
    tool_messages: list[str] = []

    for message in messages:
        if not isinstance(message, ToolMessage):
            continue

        try:
            payload = json.loads(message.content)
        except json.JSONDecodeError:
            continue

        if isinstance(payload.get("form_patch"), dict):
            form_patch.update(payload["form_patch"])

        if isinstance(payload.get("compliance_flags"), list):
            compliance_flags = payload["compliance_flags"]

        if payload.get("assistant_message"):
            tool_messages.append(str(payload["assistant_message"]))

    return {
        "form_patch": form_patch,
        "compliance_flags": compliance_flags,
        "tool_messages": tool_messages,
    }


def run_crm_agent(user_message: str, current_form: dict[str, Any]) -> dict[str, Any]:
    human_message = HumanMessage(
        content=(
            "Current form state:\n"
            f"{json.dumps(current_form, indent=2)}\n\n"
            "User message:\n"
            f"{user_message}"
        )
    )

    result = crm_agent.invoke({"messages": [human_message]})
    messages = result["messages"]
    merged = _merge_tool_outputs(messages)

    final_ai_messages = [
        message.content
        for message in messages
        if isinstance(message, AIMessage) and message.content
    ]

    assistant_message = (
        str(final_ai_messages[-1])
        if final_ai_messages
        else "I updated the interaction form."
    )

    if merged["tool_messages"] and not merged["form_patch"]:
        assistant_message = merged["tool_messages"][-1]

    return {
        "assistant_message": assistant_message,
        "form_patch": merged["form_patch"],
        "compliance_flags": merged["compliance_flags"],
    }

