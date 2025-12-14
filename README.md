# British Airways Agentic AI Chatbot



An intelligent customer service chatbot for British Airways using a multi-agent AI architecture with Retrieval-Augmented Generation (RAG).



## Features

- Multi-Agent Architecture: 4 specialized AI agents working together

- Accurate Policy-Based Responses: Uses actual BA policy documents

- Source Citations: Transparent answers with policy references

- Confidence Scores: Quality metrics for each response

- Beautiful UI: Modern, responsive chat interface

- Fast Performance: Optimized with Llama3.2:1b model



## Architecture



### Multi-Agent System

```

User Query

  ↓

Planner Agent (Analyzes query \& creates strategy)

  ↓

Retriever Agent (Searches 78 policy sections via ChromaDB)

  ↓

Reasoner Agent (Generates response with LLM)

  ↓

Evaluator Agent (Validates \& scores response)

  ↓

Response to User

```



### Tech Stack



#### Backend:

- FastAPI (Python web framework)

- Ollama + Llama3.2:1b (Local LLM)

- ChromaDB (Vector database)

- Sentence Transformers (Embeddings)



#### Frontend:

- React + Vite

- Modern CSS with animations

- Responsive design



## Quick Start



### Prerequisites



- Python 3.10+

- Node.js 18+

- Ollama



### Installation



1. Clone the repository

```bash

git clone https://github.com/tanvitiwari2004/ba-agentic-chatbot.git

cd ba-agentic-chatbot

```



2. Install Ollama and pull the model

```bash

# Install from https://ollama.ai

ollama pull llama3.2:1b

```



3. Setup Backend

```bash

cd backend

python -m venv venv



# Windows

.\\venv\\Scripts\\Activate.ps1



# Install dependencies

pip install fastapi uvicorn pydantic ollama chromadb sentence-transformers python-dotenv



# Run backend

python main.py

```



4. Setup Frontend (in a new terminal)

```bash

cd frontend

npm install

npm run dev

```



5. Open browser

```

http://localhost:5173/

```



## Project Structure

```

ba-agentic-chatbot/

├── backend/

│   ├── agents/              # AI agents

│   │   ├── planner.py       # Query analysis

│   │   ├── retriever.py     # Document retrieval

│   │   ├── reasoner.py      # Response generation

│   │   └── evaluator.py     # Quality validation

│   ├── database/

│   │   └── vector\_store.py  # ChromaDB integration

│   └── main.py              # FastAPI app

├── frontend/

│   └── src/

│       ├── App.jsx          # Main React component

│       └── App.css          # Styling

├── data/

│   └── ba\_liquids\_and\_restrictions.txt  # BA policy documents

└── README.md

```



## How It Works



1\. User asks a question about BA policies

2. Planner Agent categorizes the query (liquids, baggage, medical, etc.)

3. Retriever Agent searches 78 policy document sections using semantic search

4. Reasoner Agent generates accurate response using retrieved context

5. Evaluator Agent validates response and calculates confidence score

6. User receives accurate, policy-based answer with sources



## Key Advantages Over Traditional Chatbots



| Feature | Traditional Chatbot | Our Agentic System |

|---------|-------------------|-------------------|

| Accuracy | Generic responses | Policy-based answers from actual documents |

| Transparency | No sources | Citations with source references |

| Trust | Unknown confidence | Confidence scores (0-100%) |

| Scalability | Hardcoded rules | Automatic learning from documents |

| Maintenance | Manual updates | Just update policy documents |



## Agent Details



### Planner Agent

- Analyzes user queries

- Classifies into categories (liquids, baggage, medical, sports, etc.)

- Extracts key search terms

- Creates retrieval strategy



### Retriever Agent

- Performs semantic search over 78 policy sections

- Uses sentence transformers for embeddings

- Returns top 5 most relevant documents

- Includes fallback responses if vector store unavailable



### Reasoner Agent

- Uses Llama3.2:1b for response generation

- Strictly uses only provided context

- Optimized with temperature=0.7 and repeat\_penalty=1.2

- Prevents hallucinations (no invented information)



### Evaluator Agent

- Validates response quality

- Calculates confidence based on source relevance

- Formats citations for user display

- Ensures accuracy and completeness



## Performance Optimizations



- Faster Model: Using Llama3.2:1b instead of Llama3 (50-70% faster)

- Temperature Control: Reduced repetition with temperature=0.7

- Repeat Penalty: Prevents redundant phrasing

- Efficient Embeddings: all-MiniLM-L6-v2 for fast semantic search



## Use Cases


- Customer service automation

- Policy inquiry handling

- 24/7 availability

- Consistent, accurate responses

- Multilingual support (future enhancement)



## Future Enhancements


- Conversation memory for context-aware responses

- Multi-language support

- Voice input/output

- Integration with booking systems

- Advanced analytics dashboard

- A/B testing framework

- Deployment to cloud (AWS/Azure/GCP)



## Team

1. Tanvi Tiwari 
2. Lavanya Singh 
3. Angel Bhandari 




## Acknowledgments
- British Airways for policy documentation

\- Ollama for local LLM infrastructure

\- ChromaDB for vector database

\- FastAPI and React communities



