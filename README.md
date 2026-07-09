# AI-First CRM HCP Interaction Logger

An AI-first Customer Relationship Management (CRM) module for Healthcare Professional (HCP) interaction logging. The application provides a split-screen interface where the left panel displays a **read-only interaction form**, while the right panel contains an AI assistant chat. Users never fill the form manually—instead, the AI assistant interprets natural language prompts, selects the appropriate LangGraph tool, and automatically updates the form.

---

# Project Overview

This project is a prototype of an AI-powered CRM system designed for pharmaceutical and life sciences field representatives.

Instead of manually entering visit details after meeting a Healthcare Professional (HCP), representatives can simply describe the interaction in natural language. The AI assistant extracts structured information, updates the CRM form, performs compliance checks, suggests follow-up actions, and generates CRM-ready summaries.

The project demonstrates an AI-first workflow where LangGraph acts as the orchestration layer between the user, the LLM, and business tools.

---

# Features

- AI-controlled interaction form
- Natural language interaction logging
- AI-based field editing
- Automatic CRM summary generation
- Compliance validation for HCP interactions
- Follow-up recommendation
- Database persistence
- Read-only form controlled entirely through AI
- Split-screen CRM interface

---

# Tech Stack

### Frontend

- React
- TypeScript
- Redux Toolkit
- Vite
- Google Inter Font

### Backend

- Python
- FastAPI
- SQLAlchemy

### AI

- LangGraph
- LangChain
- Groq LLM

### LLM

Active Model:

```
llama-3.3-70b-versatile
```

**Model Note**

The assignment specified the Groq model **gemma2-9b-it**. During development, this model had been deprecated on Groq and returned a decommissioned-model error. Therefore, **llama-3.3-70b-versatile** was used as a compatible replacement. The model can be changed at any time through the `GROQ_MODEL` environment variable without modifying the application code.

### Database

The application uses **SQLAlchemy with SQLite** for local demonstration.

The project is fully compatible with **PostgreSQL** or **MySQL** by simply changing the `DATABASE_URL` environment variable.

---

# System Architecture

```text
                   React + Redux
                         │
               POST /api/chat
                         │
                     FastAPI
                         │
                    LangGraph
                         │
      ┌────────────┬─────────────┬─────────────┐
      │            │             │             │
 Log Tool     Edit Tool   Compliance Tool   Summary Tool
      │            │             │             │
      └────────────┴─────────────┴─────────────┘
                         │
                     Groq LLM
                         │
                    SQLAlchemy
                         │
                      SQLite
```

---

# Project Structure

```text
hcp-crm-ai/

├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── graph.py
│   │   │   └── tools.py
│   │   ├── services/
│   │   │   └── interaction_service.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   ├── components/
│   │   ├── features/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── styles.css
│   ├── package.json
│   └── tsconfig.json
│
├── README.md
└── .gitignore
```

---

# How the Application Works

```text
User enters a natural language prompt
            │
            ▼
React sends the prompt to FastAPI
            │
            ▼
FastAPI invokes the LangGraph agent
            │
            ▼
Groq LLM determines the user's intent
            │
            ▼
LangGraph selects the appropriate tool
            │
            ▼
The selected tool returns a structured form patch
            │
            ▼
Redux updates the application state
            │
            ▼
The read-only CRM form updates automatically
```

---

# LangGraph Tools

The project implements five LangGraph tools located in:

```
backend/app/agent/tools.py
```

---

## 1. Log Interaction Tool

### Purpose

Extracts HCP interaction details from natural language and automatically fills the interaction form.

### Example Prompt

```text
I met Dr. Priya Menon yesterday at Fortis Hospital. She is an endocrinologist. We discussed GlucoFree. She was positive and requested adherence data.
```

### Expected Output

- HCP Name
- Specialty
- Institution
- Product
- Sentiment
- Key Topics
- Follow-up Required

---

## 2. Edit Interaction Tool

### Purpose

Updates existing interaction details using natural language without manually editing the form.

### Example Prompt

```text
Change the sentiment to Neutral and set the interaction type to in-person visit.
```

### Expected Output

Only the requested fields are updated while preserving all other information.

---

## 3. Validate Compliance Tool

### Purpose

Reviews interaction notes for potential compliance concerns commonly found in regulated life sciences interactions.

### Example Prompt

```text
Check this interaction for compliance:
I promised guaranteed patient improvement and offered a gift if the doctor prescribed GlucoFree.
```

### Expected Output

- Compliance warnings
- Flagged risk statements
- Compliance status update

---

## 4. Suggest Follow-up Tool

### Purpose

Recommends the next best action based on the interaction.

### Example Prompt

```text
The doctor requested approved adherence data next week.
```

### Expected Output

- Follow-up required
- Suggested next action
- Reminder recommendation

---

## 5. Summarize Interaction Tool

### Purpose

Converts rough meeting notes into professional CRM-ready documentation.

### Example Prompt

```text
Make this CRM-ready:
met doctor today discussed GlucoFree she liked data but requested more adherence information no samples provided
```

### Expected Output

A concise and professional CRM summary.

---

# Backend Setup

```powershell
cd backend

python -m venv ..\.venv

..\ .venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

Create a file named:

```
backend/.env
```

Example:

```env
GROQ_API_KEY=your_groq_api_key

GROQ_MODEL=llama-3.3-70b-versatile

DATABASE_URL=sqlite:///./hcp_crm.db
```

Run the backend:

```powershell
python -m uvicorn app.main:app --reload
```

Backend URLs

```
http://127.0.0.1:8000/api/health

http://127.0.0.1:8000/docs
```

---

# Frontend Setup

```powershell
cd frontend

npm install

npm run dev
```

Frontend URL

```
http://localhost:5173
```

---

# Demo Flow

1. Launch the frontend.
2. Show the split-screen interface.
3. Explain that the interaction form is read-only.
4. Demonstrate Log Interaction.
5. Demonstrate Edit Interaction.
6. Demonstrate Compliance Validation.
7. Demonstrate Follow-up Recommendation.
8. Demonstrate CRM Summary Generation.
9. Click **Save Interaction**.
10. Show the generated interaction ID.

---

# Code Walkthrough

### Backend

- `app/main.py` – FastAPI application and REST APIs
- `agent/graph.py` – LangGraph workflow
- `agent/tools.py` – LangGraph tools
- `database.py` – SQLAlchemy database configuration
- `models.py` – Database models
- `schemas.py` – Request and response schemas
- `services/interaction_service.py` – Business logic

### Frontend

- `InteractionForm.tsx` – Read-only CRM form
- `AIAssistantPanel.tsx` – AI chat interface
- `interactionSlice.ts` – Redux interaction state
- `chatSlice.ts` – Chat state management
- `store.ts` – Redux store

---

# Future Enhancements

- Authentication and role-based access
- PostgreSQL production deployment
- MySQL production deployment
- Multi-user CRM support
- Calendar integration
- Email reminders
- Doctor interaction history
- File attachments
- Dashboard and analytics
- Voice-based interaction logging

---

# Assignment Summary

This project demonstrates an AI-first CRM workflow for Healthcare Professional interaction logging.

The application satisfies the assignment requirements by implementing:

- React frontend
- Redux state management
- FastAPI backend
- LangGraph agent orchestration
- Groq LLM integration
- Five LangGraph tools
- Automatic AI-controlled form population
- Database persistence
- Natural language interaction editing
- Split-screen CRM interface
