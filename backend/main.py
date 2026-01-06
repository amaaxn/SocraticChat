from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import openai
from openai import OpenAIError
import os
from dotenv import load_dotenv
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

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable is required")
    raise ValueError("OPENAI_API_KEY environment variable is required. Please set it in your .env file or environment variables.")

openai_client = openai.OpenAI(api_key=api_key)

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
except (ImportError, OSError) as e:
    logger.warning(f"spaCy not available: {e}. Text preprocessing will be limited.")
    nlp = None

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    processed_input: Optional[str] = None

sessions = {}

def get_system_message():
    """Returns the system message for Socratic dialogue."""
    return {
        "role": "system",
        "content": "You are a Socratic teacher engaging in thoughtful dialogue. Your goal is to help users think deeply by asking probing questions rather than providing direct answers. Guide them through their reasoning process, challenge assumptions gently, and encourage critical thinking. Keep responses concise and conversational."
    }

def preprocess_text(text: str) -> str:
    """
    Preprocess text using NLP: tokenization, lemmatization, and stop word removal.
    Falls back to simple lowercase if spaCy is not available.
    """
    if nlp is None:
        return text.lower().strip()
    
    doc = nlp(text)
    processed_tokens = [
        token.lemma_.lower() 
        for token in doc 
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return " ".join(processed_tokens)

def generate_socratic_response(user_message: str, conversation_history: List[dict]) -> str:
    """
    Generate a Socratic-style response using GPT-4.
    Handles API errors including rate limits and authentication issues.
    """
    messages = [get_system_message()]
    
    for msg in conversation_history[-6:]:
        messages.append(msg)
    
    messages.append({"role": "user", "content": user_message})
    
    try:
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
    except OpenAIError as e:
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
    """
    Main chat endpoint that processes user messages and returns Socratic responses.
    Applies NLP preprocessing and maintains conversation context.
    """
    user_input = chat_message.message.strip()
    
    if not user_input:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    session_id = chat_message.session_id or f"session_{datetime.now().timestamp()}"
    if session_id not in sessions:
        sessions[session_id] = []
    
    processed_input = preprocess_text(user_input)
    logger.info(f"Processed input: {processed_input}")
    
    sessions[session_id].append({"role": "user", "content": user_input})
    
    try:
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
