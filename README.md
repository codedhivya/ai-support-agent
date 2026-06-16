# AI Support Agent (RAG)

An intelligent, context-aware AI Customer Support Agent application powered by a **Retrieval-Augmented Generation (RAG)** architecture. Users can upload support manuals, knowledge bases, and documentations (PDF/TXT), and chat with an AI assistant that answers questions based directly on the uploaded documents.

---

## System Architecture

The project uses a standard monorepo structure separating the Python backend and Next.js frontend:

```mermaid
graph TD
    subgraph Client Space
        Browser["Next.js Web Frontend"]
    end

    subgraph App Server
        FastAPI["FastAPI App Server"]
    end

    subgraph Storage & AI Services
        Postgres["RDS PostgreSQL (with pgvector)"]
        S3["Amazon S3 (Doc Uploads)"]
        OpenAI["OpenAI API (Embeddings & Chat)"]
    end

    Browser ──►|HTTPS (via Next.js Rewrite)| FastAPI
    FastAPI ──►|SQL Queries| Postgres
    FastAPI ──►|File Uploads| S3
    FastAPI ──►|text-embedding-3-small| OpenAI
    FastAPI ──►|gpt-4o-mini| OpenAI
```

### Flow of Operations:
1. **Document Ingestion:** Pushing a document extracts its text, splits it recursively into cohesive chunks, converts them to 1536-dimensional vectors using OpenAI's embedding API, and stores them in PostgreSQL using `pgvector`.
2. **Retrieval (Semantic Search):** When a user asks a question, the question is vectorized, and a cosine distance query (`<=>`) is run in the database to fetch the top 5 most relevant document chunks.
3. **Generation:** The context chunks and chat history are fed to GPT-4o-mini to generate a highly accurate, cited response.

---

## Tech Stack

* **Frontend:** Next.js (App Router), React, TypeScript, Axios, Tailwind CSS, hosted on **AWS Amplify**.
* **Backend:** FastAPI, Python, SQLAlchemy, Uvicorn, Docker, hosted on **AWS ECS Fargate**.
* **Database:** PostgreSQL (with `pgvector` extension enabled) on **AWS RDS**.
* **CI/CD:** GitHub Actions (for backend tests, Docker packaging, and automated ECS rolling deployments).

---

## Local Development Setup

### 1. Prerequisites
* Python 3.10+
* Node.js 18+
* PostgreSQL database with `pgvector` extension installed.

### 2. Backend Setup
1. Navigate to the backend folder:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend/` directory:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
   OPENAI_API_KEY=your-openai-api-key
   ```
5. Initialize the database schema:
   ```bash
   python app/db/init_db.py
   ```
6. Run the local development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### 3. Frontend Setup
1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Create a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. Visit `http://localhost:3000` to interact with the application.

---

## Automated Testing

Backend unit tests are written with `pytest` and `httpx`. To run tests locally:
```bash
cd backend
DATABASE_URL=sqlite:///test.db OPENAI_API_KEY=mock python -m pytest
```

---

## CI/CD and AWS Deployment

The project is configured for automated deployments triggered on merges to the `main` branch:

* **Frontend Deployment:** Automated via **AWS Amplify Hosting**. It is connected directly to the GitHub repository branch and builds SSR Next.js using the defined environment variable `NEXT_PUBLIC_API_URL`.
* **Backend Deployment:** Automated via **GitHub Actions** (`.github/workflows/backend_deploy.yml`):
  1. Sets up Python and installs dependencies.
  2. Runs the unit test suite (`pytest`).
  3. Packages the FastAPI application into a Docker container.
  4. Pushes the image to **Amazon ECR**.
  5. Forces a rolling update to the **Amazon ECS Fargate** cluster.
