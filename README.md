# British Airways Agentic Chatbot

This project implements an advanced AI-driven customer service agent tailored for British Airways. Utilizing a multi-agent architecture, the system is capable of planning, retrieving, reasoning, and evaluating responses to provide accurate and context-aware assistance regarding travel policies, baggage allowances, and liquid restrictions.

## Key Features

*   **Multi-Agent Architecture**: Orchestrates four specialized agents (Planner, Retriever, Reasoner, Evaluator) to handle complex queries intelligently.
*   **Retrieval-Augmented Generation (RAG)**: Leverages OpenAI Embeddings and ChromaDB to perform semantic searches through official policy documents, ensuring responses are grounded in fact.
*   **Continuous Improvement**: Includes a feedback mechanism that captures user satisfaction and specific issues to facilitate offline model refinement and learning.
*   **Containerization**: A fully dockerized application ensuring consistent deployment and execution across different environments.
*   **Automated Quality Assurance**: Integrated CI/CD workflows via GitHub Actions for automated code linting and build verification.
*   **Modern User Interface**: Features a responsive React-based frontend designed with the British Airways visual identity.

## System Architecture

The application defines a structured workflow to ensure reliability and accuracy:

1.  **Planner Agent**: Analyzes the user's intent to determine if the query relates to specific policies or general information, formulating a targeted search strategy.
2.  **Retriever Agent**: Queries the vector database to fetch the most relevant sections of the policy documents.
3.  **Reasoner Agent**: Synthesizes a natural language response using the retrieved data and the ongoing conversation history.
4.  **Evaluator Agent**: Independently verifies the generated response against the source material to prevent hallucinations before the message is sent to the user.

For a visual representation of this workflow, please refer to the [System Architecture Document](system_architecture.md).

## Technology Stack

*   **Frontend**: React, Vite, Nginx
*   **Backend**: Python, FastAPI, Uvicorn
*   **AI & Data**: OpenAI GPT-4o-mini, ChromaDB, LangChain concepts
*   **Infrastructure**: Docker, Docker Compose, GitHub Actions

## High Level Setup Guide

### Prerequisites

Ensure you have the following installed:
*   Docker Desktop
*   Git

You will also need a valid OpenAI API Key.

### Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/tanvitiwari2004/ba-agentic-chatbot.git
    cd ba-agentic-chatbot
    ```

2.  **Configure Environment**:
    Set up the backend environment variables by copying the example file. Open the created `.env` file and input your API key.
    ```bash
    # Windows (PowerShell)
    cp backend/.env.example backend/.env
    ```

3.  **Run the Application**:
    Use Docker Compose to build and start all services.
    ```bash
    docker compose up --build
    ```

4.  **Access the Application**:
    *   The Chatbot Interface is available at: http://localhost
    *   The Backend API Documentation is available at: http://localhost:8000/docs

## Testing and Verification

The system includes built-in logging to demonstrate the decision-making process of the agents. You can view these logs to understand how the system processes a query:

```bash
docker compose logs -f backend
```

## Contributing

Contributions are welcome. Please fork the repository, create a feature branch, and submit a pull request for review.


