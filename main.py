from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import phospho
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from groq import Groq
from supabase import create_client

from common.api_global_variables import api_global_variables
from common.constants import (
    GROQ_API_KEY,
    PHOSPHO_API_KEY,
    PHOSPHO_PROJECT_ID,
    SUPABASE_API_KEY,
    SUPABASE_URL,
)
from common.embedder import Embedder
from common.llm import call_groq
from common.schemas import ConversationDto


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Load clients when the app starts.

    FastAPI doc about lifespan events: https://fastapi.tiangolo.com/advanced/events/.
    """

    if SUPABASE_URL and SUPABASE_API_KEY:
        api_global_variables.supabase_client = create_client(
            SUPABASE_URL, SUPABASE_API_KEY
        )
    else:
        raise ValueError("Supabase URL or Key missing")

    api_global_variables.llm = Groq(
        api_key=GROQ_API_KEY,
    )

    phospho.init(api_key=PHOSPHO_API_KEY, project_id=PHOSPHO_PROJECT_ID)

    # api_global_variables.qdrant_client = QdrantClient(
    #     host=QDRANT_HOST, port=QDRANT_PORT
    # )
    api_global_variables.embedder = Embedder()

    yield

    # api_global_variables.qdrant_client.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "OK"}, 200


@app.get("/conversations")
async def get_conversations():
    response = (
        api_global_variables.supabase_client.table("conversations")
        .select("*")
        .execute()
    )
    return response.data


@app.post("/conversations")
async def create_user(conversationDto: ConversationDto):
    response = (
        api_global_variables.supabase_client.table("conversations")
        .insert({"id": conversationDto.id, "message": conversationDto.message})
        .execute()
    )

    if not response.data:
        raise HTTPException(status_code=400, detail="Failed to create user")

    return response.data[0]


@app.post("/test-phospho")
async def test_phospho(question: str):
    return call_groq(question)


@app.post("/embedding")
async def embbed_file(request: Request):
    data = await request.json()
    vector = data.get("vector")
    payload = data.get("payload")
    if vector:
        api_global_variables.qdrant_client.upsert(
            collection_name="your_collection",
            points=[{"id": "unique-id", "vector": vector, "payload": payload}],
        )
        return {"message": "Vector added successfully"}
    raise HTTPException(status_code=400, detail="Vector data missing")


@app.post("/search")
async def search_vector(request: Request):
    data = await request.json()
    query_vector = data.get("vector")
    if query_vector:
        result = api_global_variables.qdrant_client.search(
            collection_name="your_collection", query_vector=query_vector, limit=5
        )
        return result
    raise HTTPException(status_code=400, detail="Query vector missing")
