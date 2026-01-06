from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import openai
import os
from dotenv import load_dotenv
import spacy
import logging
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="SocraticChat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai_client = None
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    openai_client = openai.OpenAI(api_key=api_key)
else:
    logger.warning("OPENAI_API_KEY not found in environment variables")

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    logger.warning("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    nlp = None

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    processed_input: Optional[str] = None

sessions = {}

def preprocess_text(text: str) -> str:
    if nlp is None:
        return text
    
    doc = nlp(text)
    processed_tokens = [
        token.lemma_.lower() 
        for token in doc 
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return " ".join(processed_tokens)

def generate_socratic_response(user_message: str, conversation_history: List[dict]) -> str:
    try:
        messages = [
            {
                "role": "system",
                "content": """You are a Socratic teacher engaging in thoughtful dialogue. 
                Your goal is to help users think deeply by asking probing questions rather than 
                providing direct answers. Guide them through their reasoning process, challenge 
                assumptions gently, and encourage critical thinking. Keep responses concise and 
                conversational."""
            }
        ]
        
        for msg in conversation_history[-6:]:
            messages.append(msg)
        
        messages.append({"role": "user", "content": user_message})
        
        if not openai_client:
            raise HTTPException(
                status_code=500,
                detail="OpenAI API key not configured"
            )
        
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content.strip()
    
    except openai.RateLimitError:
        logger.error("OpenAI API rate limit exceeded")
        raise HTTPException(
            status_code=429,
            detail="API rate limit exceeded. Please try again in a moment."
        )
    except openai.AuthenticationError:
        logger.error("OpenAI API authentication failed")
        raise HTTPException(
            status_code=401,
            detail="API authentication failed. Please check your API key."
        )
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"API error occurred: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again."
        )

@app.get("/")
def root():
    return {"message": "SocraticChat API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/chat", response_model=ChatResponse)
async def chat(chat_message: ChatMessage):
    try:
        user_input = chat_message.message.strip()
        
        if not user_input:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        session_id = chat_message.session_id or f"session_{datetime.now().timestamp()}"
        if session_id not in sessions:
            sessions[session_id] = []
        
        processed_input = preprocess_text(user_input)
        logger.info(f"Processed input: {processed_input}")
        
        sessions[session_id].append({"role": "user", "content": user_input})
        
        response_text = generate_socratic_response(user_input, sessions[session_id])
        
        sessions[session_id].append({"role": "assistant", "content": response_text})
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            processed_input=processed_input
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat: {str(e)}"
        )

@app.get("/sessions/{session_id}")
def get_session_history(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": session_id, "history": sessions[session_id]}

@app.delete("/sessions/{session_id}")
def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session cleared", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
