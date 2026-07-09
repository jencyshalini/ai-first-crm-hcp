# AI-First CRM HCP Interaction Logger

This project is an AI-first Customer Relationship Management module for Healthcare Professional interaction logging. It uses a split-screen interface where the left side shows a read-only HCP interaction form and the right side provides an AI assistant chat. The user does not manually fill the form; the AI assistant controls the form through natural language prompts.

## Task Understanding

The goal was to build a technical prototype of a life-sciences CRM screen for field representatives. A representative can describe an HCP meeting, correction, follow-up request, or compliance concern in natural language. The AI assistant interprets the message, calls LangGraph tools, and returns structured form updates to the React frontend.

The application demonstrates:

- AI-controlled form population
- Natural-language field editing
- Compliance review for regulated HCP interactions
- Follow-up recommendation
- CRM-ready note summarization
- Database save flow

## Tech Stack

- Frontend: React, TypeScript, Redux Toolkit, Vite
- Backend: Python, FastAPI
- AI Framework: LangGraph
- LLM Provider: Groq through LangChain `ChatGroq`
- Active Groq Model: `llama-3.3-70b-versatile`
- Requested Model Note: `gemma2-9b-it` was requested in the assignment, but Groq returned a decommissioned-model error. The model is configurable with `GROQ_MODEL`.
- Database: SQLAlchemy with SQLite for local demo, compatible with Postgres/MySQL through `DATABASE_URL`
- Font: Google Inter

## Project Structure

```text
hcp-crm-ai/
  backend/
    app/
      agent/
        graph.py
        tools.py
      services/
        interaction_service.py
      database.py
      main.py
      models.py
      schemas.py
    requirements.txt
    .env.example
  frontend/
    src/
      app/
        hooks.ts
        store.ts
      components/
        AIAssistantPanel.tsx
        InteractionForm.tsx
      features/
        chat/
          chatSlice.ts
        interaction/
          interactionSlice.ts
      App.tsx
      main.tsx
      styles.css
    package.json
```

## How The App Works

```text
User writes message in chat
  -> React sends message and current form state to FastAPI
  -> FastAPI calls the LangGraph agent
  -> Groq LLM decides which tool to call
  -> Tool returns a structured form_patch
  -> Redux applies the patch
  -> Left-side CRM form updates automatically
```

## LangGraph Tools

The project implements five LangGraph tools in `backend/app/agent/tools.py`.

### 1. Log Interaction Tool

Purpose: Extracts HCP interaction details from a natural-language note and fills the form.

Example prompt:

```text
I met Dr. Priya Menon yesterday at Fortis. She is an endocrinologist. We discussed GlucoFree. She was positive and asked for adherence data.
```

Expected behavior:

- Fills HCP name
- Fills specialty
- Fills institution
- Fills product discussed
- Sets sentiment
- Adds key topics
- Adds follow-up requirement

### 2. Edit Interaction Tool

Purpose: Updates specific fields when the AI-filled form has a mistake.

Example prompt:

```text
Change the sentiment to Neutral and set the interaction type to in-person visit.
```

Expected behavior:

- Updates sentiment
- Updates interaction type
- Does not require manual form editing

### 3. Validate Compliance Tool

Purpose: Checks interaction notes for common regulated life-sciences risks.

Example prompt:

```text
Check this note for compliance: I promised the doctor guaranteed patient improvement and offered a gift if they prescribe GlucoFree.
```

Expected behavior:

- Flags possible guarantee or overstatement
- Flags possible gift or inducement concern
- Updates compliance flags

### 4. Suggest Follow-up Tool

Purpose: Recommends next steps based on sentiment, key topics, and requested materials.

Example prompt:

```text
The doctor was interested and asked me to send approved adherence data next week.
```

Expected behavior:

- Sets follow-up required to true
- Suggests sending approved material
- Keeps the interaction in Draft until saved

### 5. Summarize Interaction Tool

Purpose: Converts rough representative notes into a cleaner CRM-ready summary.

Example prompt:

```text
Make this CRM-ready: met doctor today discussed GlucoFree she liked data but wants more adherence info no samples given.
```

Expected behavior:

- Updates discussion summary
- Produces a concise CRM-style note

## Backend Setup

```powershell
cd D:\projects\hcp-crm-ai\backend
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
DATABASE_URL=sqlite:///./hcp_crm.db
```

Run backend:

```powershell
python -m uvicorn app.main:app --reload
```

Backend URLs:

```text
http://127.0.0.1:8000/api/health
http://127.0.0.1:8000/docs
```

## Frontend Setup

```powershell
cd D:\projects\hcp-crm-ai\frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Demo Flow

1. Open the frontend.
2. Show the left read-only interaction form.
3. Show the right AI assistant panel.
4. Enter the log interaction prompt.
5. Show the form automatically filling.
6. Enter the edit interaction prompt.
7. Show the fields changing without manual form input.
8. Enter the compliance prompt.
9. Show compliance flags.
10. Enter the follow-up prompt.
11. Show follow-up fields.
12. Enter the summarization prompt.
13. Show discussion summary update.
14. Click Save Interaction.
15. Show saved interaction ID.

## Video Walkthrough Script

Recommended length: 10 to 15 minutes.

### 1. Introduction

Explain that this is an AI-first HCP CRM interaction logger for life-sciences field representatives. The key idea is that the form is controlled through chat, not manual typing.

### 2. Frontend Walkthrough

Show the split-screen UI:

- Left panel: interaction details form
- Right panel: AI assistant chat
- Form fields are disabled/read-only
- Save button appears after the form is populated

### 3. Tool Demo

Run these prompts one by one:

```text
I met Dr. Priya Menon yesterday at Fortis. She is an endocrinologist. We discussed GlucoFree. She was positive and asked for adherence data.
```

```text
Change the sentiment to Neutral and set the interaction type to in-person visit.
```

```text
Check this note for compliance: I promised the doctor guaranteed patient improvement and offered a gift if they prescribe GlucoFree.
```

```text
The doctor was interested and asked me to send approved adherence data next week.
```

```text
Make this CRM-ready: met doctor today discussed GlucoFree she liked data but wants more adherence info no samples given.
```

Explain which LangGraph tool is being demonstrated after each prompt.

### 4. Code Explanation

Briefly show:

- `backend/app/agent/tools.py` for the five tools
- `backend/app/agent/graph.py` for LangGraph orchestration
- `backend/app/main.py` for FastAPI endpoints
- `frontend/src/features/interaction/interactionSlice.ts` for Redux form state
- `frontend/src/features/chat/chatSlice.ts` for chat API calls
- `frontend/src/components/InteractionForm.tsx` for the read-only form
- `frontend/src/components/AIAssistantPanel.tsx` for the chat panel

### 5. Database Save

Click Save Interaction and explain that the saved record goes through FastAPI and SQLAlchemy into the local database.

### 6. Summary

Summarize that the project satisfies the requirement by using React, Redux, FastAPI, LangGraph, Groq LLM, SQLAlchemy database persistence, and five AI tools.

## GitHub Deployment Steps

```powershell
cd D:\projects\hcp-crm-ai
git init
git add .
git commit -m "Build AI-first HCP CRM interaction logger"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/hcp-crm-ai.git
git push -u origin main
```

Do not commit `.env`. Add this to `.gitignore`:

```text
backend/.env
backend/hcp_crm.db
backend/__pycache__/
backend/app/__pycache__/
backend/app/agent/__pycache__/
backend/app/services/__pycache__/
frontend/node_modules/
frontend/dist/
```

