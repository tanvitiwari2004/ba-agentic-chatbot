# British Airways Agentic Chatbot - System Architecture

## Overview
This document outlines the technical architecture of the British Airways Agentic Chatbot. The system is built as a microservices application using Docker, featuring a React frontend and a FastAPI backend that orchestrates a multi-agent AI system.

## High-Level Architecture

```mermaid
graph TD
    %% Styling
    classDef frontend fill:#E1F5FE,stroke:#01579B,stroke-width:2px;
    classDef backend fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px;
    classDef external fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px;
    classDef storage fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px;

    %% User Interaction
    User([Customer]) -->|HTTPS| Frontend[React Frontend];
    
    %% Frontend
    subgraph Client Application
        Frontend -->|REST API /chat| API[FastAPI Backend];
        Frontend -->|REST API /feedback| API;
    end

    %% Backend Agents
    subgraph Agentic Core
        API -->|Orchestrates| Memory[Conversation Memory];
        API -->|Step 1| Planner[Planner Agent];
        API -->|Step 2| Retriever[Retriever Agent];
        API -->|Step 3| Reasoner[Reasoner Agent];
        API -->|Step 4| Evaluator[Evaluator Agent];
        
        Planner -->|Analyze Intent| OpenAI[OpenAI GPT-4o];
        Reasoner -->|Generate Answer| OpenAI;
        Evaluator -->|Verify Factuality| OpenAI;
    end

    %% Data Layer
    subgraph Data & Storage
        Retriever -->|Semantic Search| VectorStore[(ChromaDB)];
        VectorStore -->|Embeddings| OpenAI;
        API -->|Persist Feedback| FeedbackLog[feedback_history.json];
        Memory -->|Store History| InMemory[In-Memory Session];
    end

    %% Class Assignment
    class Frontend frontend;
    class API,Planner,Retriever,Reasoner,Evaluator backend;
    class OpenAI external;
    class VectorStore,FeedbackLog,Memory,InMemory storage;
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
