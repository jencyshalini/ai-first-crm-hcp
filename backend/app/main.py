from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.agent.graph import run_crm_agent
from app.database import create_tables, get_db
from app.schemas import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    InteractionCreate,
    InteractionResponse,
)
from app.services.interaction_service import create_interaction, list_interactions


app = FastAPI(
    title="AI-First HCP CRM API",
    description="Backend API for the AI-controlled HCP interaction logging screen.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    create_tables()


@app.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="hcp-crm-api")


@app.post("/api/agent/message", response_model=ChatResponse)
def agent_message(request: ChatRequest) -> ChatResponse:
    result = run_crm_agent(request.message, request.current_form)
    return ChatResponse(**result)


@app.post("/api/interactions", response_model=InteractionResponse)
def save_interaction(
    interaction: InteractionCreate,
    db: Session = Depends(get_db),
) -> InteractionResponse:
    return create_interaction(db, interaction)


@app.get("/api/interactions", response_model=list[InteractionResponse])
def get_interactions(db: Session = Depends(get_db)) -> list[InteractionResponse]:
    return list_interactions(db)
