# British Airways Agentic Chatbot - System Architecture

## Overview
This document outlines the technical architecture of the British Airways Agentic Chatbot. The system is built as a microservices application using Docker, featuring a React frontend and a FastAPI backend that orchestrates a multi-agent AI system.

## High-Level Architecture

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontSize': '20px', 'fontFamily': 'arial', 'primaryColor': '#ffffff', 'edgeLabelBackground':'#ffffff', 'tertiaryColor': '#f4f4f4'}}}%%
graph TD
    %% Styling
    classDef main fill:#fff,stroke:#00295A,stroke-width:2px,rx:10,ry:10;
    classDef agent fill:#EDF2F7,stroke:#00295A,stroke-width:2px,rx:5,ry:5;
    classDef db fill:#ebebff,stroke:#555,stroke-width:2px;

    User([Customer]) -->|1. Asks Question| UI[Frontend Interface]
    UI -->|2. POST /chat| API[Backend Orchestrator]

    subgraph "Agentic Workflow (Linear Chain)"
        direction TB
        API -->|3. Analyze| Plan[1. Planner Agent]
        Plan -->|4. Search Plan| Ret[2. Retriever Agent]
        Ret <-->|5. Semantic Search| VDB[(Vector Database)]
        Ret -->|6. Retrieved Facts| Reas[3. Reasoner Agent]
        Reas -->|7. Generate Draft| Eval[4. Evaluator Agent]
    end

    Eval -->|8. Verified Final Answer| API
    API -->|9. Response| UI
    
    class User,UI,API main;
    class Plan,Ret,Reas,Eval agent;
    class VDB db;
```

## Component Details

### 1. Frontend (React + Vite)
- **Role**: Provides the chat interface.
- **Features**: Glassmorphism UI, real-time typing indicators, markdown support, and an integrated feedback collection flow.
- **Communication**: Sends requests to the backend via REST `POST /chat`.

### 2. Backend (FastAPI)
- **Role**: Central orchestrator.
- **Agents**:
    - **Planner Agent**: Analyzes user intent (e.g., "Liquids" vs. "Baggage") and creates a search strategy.
    - **Retriever Agent**: Queries the `ChromaDB` vector store using OpenAI Embeddings to find relevant BA policies.
    - **Reasoner Agent**: Synthesizes the final answer using the relevant context and conversation history, ensuring politeness and accuracy.
    - **Evaluator Agent**: Self-corrects the output by verifying the generated answer against the retrieved sources before sending it to the user.

### 3. Data & Storage
- **ChromaDB**: Stores vector embeddings of British Airways policy documents for semantic search.
- **OpenAI**: Provides LLM capabilities (`gpt-4o-mini`) and Embeddings (`text-embedding-3-small`).
- **Feedback Loop**: User feedback (Satisfied/Not Satisfied) is logged to `feedback_history.json` for future offline learning and model fine-tuning.

## Docker Infrastructure
The entire system is containerized for easy deployment:
- **Frontend Container**: Nginx serving the React build.
- **Backend Container**: Python 3.10-slim running Uvicorn/FastAPI.
- **Networking**: Containers communicate via a private Docker bridge network.
