# AI-Assisted Reporting (QuerySense)

This repository contains the source code for QuerySense, an AI-assisted reporting and data analysis application. It provides a conversational interface over database records, allowing users to query and analyze data using natural language.

The application is split into a Django/PostgreSQL backend and a React (Vite) frontend.

## Architecture & Implementation Details

- **Streaming AI Responses**: The chat interface uses Server-Sent Events (SSE) via a POST-based `fetch` implementation. This supports streaming real-time status updates (e.g., "Querying database...", "Thinking...") alongside the final AI response.
- **Data Ingestion**: Large file uploads are handled via a chunked upload mechanism in Django to prevent memory exhaustion and timeout issues on large datasets.
- **Vector Search**: The database uses PostgreSQL with the `pgvector` extension to store and query embeddings for Retrieval-Augmented Generation (RAG) workflows.
- **Frontend**: Built with React 19, TypeScript, Tailwind CSS v4, and shadcn/ui.
- **Authentication**: JWT-based auth via `SimpleJWT` for the API, handling login and registration flows.

## Tech Stack

- **Backend**: Django 6.0, Django REST Framework, PostgreSQL 15, pgvector, scikit-learn, NumPy.
- **Frontend**: React 19, Vite, TypeScript, Tailwind CSS.
- **Infrastructure**: Docker & Docker Compose for orchestration.

## Local Development Setup

We use Docker Compose to spin up the local development environment, including the Postgres database, backend API, and frontend dev server.

### Prerequisites
- Docker and Docker Compose
- Node.js (if running the frontend natively)
- Python 3.11+ (if running the backend natively)

### Running via Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AI-Assited-Reporting.git
   cd AI-Assited-Reporting
   ```

2. Create a `.env` file in the project root. Be sure to configure the connection variables for the source database that the application will query against:
   ```env
   # Source DB Connection
   SOURCE_DB_NAME=your_db_name
   SOURCE_DB_USER=your_db_user
   SOURCE_DB_PASSWORD=your_db_password
   SOURCE_DB_HOST=your_db_host
   SOURCE_DB_PORT=5432
   SOURCE_DB_TYPE=django.db.backends.postgresql
   ```

3. Build and bring up the containers:
   ```bash
   docker-compose up --build
   ```

4. Run migrations for the application's internal database:
   ```bash
   docker-compose exec backend python manage.py migrate
   ```

   The services will be active and exposed at:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Database Seeding

To seed the initial database with sample reporting data for local development, run the custom management command inside the backend container:

```bash
docker-compose exec backend python manage.py seed_db
```

## Directory Structure

- `backend/`: Django project housing the REST API, AI processing logic (`ai/`), and user management (`users/`).
- `frontend/`: React application containing UI components, route views, and SSE client integration. 
- `docker-compose.yml`: Local orchestrator configuration.
