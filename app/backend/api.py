from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Literal
from dotenv import load_dotenv

from app.core.ai_agent import get_response_from_ai_agents
from app.config.settings import settings

load_dotenv()

app = FastAPI(title="Multi AI Agent LLMOPS API")


# 🔥 message schema
class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str


class RequestState(BaseModel):
    model_name: str
    system_prompt: str
    messages: List[Message]
    allow_search: bool = False
    session_id: str  


session_store = {}


@app.post("/chat")
def chat_endpoint(request: RequestState):

    if request.model_name not in settings.ALLOWED_MODEL_NAMES:
        raise HTTPException(status_code=400, detail="Invalid model")

    session_id = request.session_id

    # get history
    history = session_store.get(session_id, [])

    new_msgs = [m.dict() for m in request.messages]
    history.extend(new_msgs)

    try:
        response = get_response_from_ai_agents(
            request.model_name,
            history,
            request.system_prompt,
            request.allow_search
        )

        history.append({
            "role": "assistant",
            "content": response
        })

        session_store[session_id] = history

        return {"response": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))