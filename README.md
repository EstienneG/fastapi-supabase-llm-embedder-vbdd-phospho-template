# FastAPI Backend

## Overview

This is a FastAPI backend project that uses:
- **Supabase** as the primary database.
- **OpenAI API** for embedding.
- **Groq** as llm provider.
- **Qdrant** as a vector database.

Follow the steps below to set up your environment, install dependencies, and run the server.

---

## Prerequisites

- **Python**: Ensure you have Python 3.12 or later installed. You can check your version with:
  ```bash
  python --version

Virtual Environment: It’s recommended to use a virtual environment to manage dependencies.

# Project Setup

## 1. Set Up Environment Variables
Copy .env.example file in the project root and add the following environment variables:

```bash
  # OpenAI API for embedding
  PHOSPHO_API_KEY=<your_phospho_api_key>
  PHOSPHO_PROJECT_ID=<your_phospho_project_id>
  GROQ_API_KEY=<your_groq_api_key>
  OPENAI_API_KEY=<your_openai_api_key>

  SUPABASE_URL=<your_supabase_url>
  SUPABASE_API_KEY=<your_supabase_api_key>
```

Replace keys with your keys.

## 2. Install Dependencies
Create and activate a virtual environment, then install dependencies:

```bash
  # Create a virtual environment
  python -m venv venv

  # Activate the virtual environment
  # On Windows
  venv\Scripts\activate
  # On macOS/Linux
  source venv/bin/activate

  # Install dependencies
  pip install -r requirements.txt
```

## 3. Start the FastAPI Server
Run the FastAPI server locally with:

```bash
  uvicorn main:app --reload
```