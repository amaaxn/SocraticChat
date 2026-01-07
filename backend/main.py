import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from fastapi import FastAPI
from pydantic import BaseModel
import spacy
from fastapi.middleware.cors import CORSMiddleware
from collections import defaultdict




load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is required")

def populateRole():
   return [{"role": "system", "content" : "Use the Socratic method in order to respond with thoughtful questions that challenge assumptions and encourage deeper thinking. Answer in one line and at most a paragraph, abd respond like a patient and insightful tutor."}]

histories = defaultdict(lambda: populateRole())

try:
   nlp = spacy.load("en_core_web_sm")
except (ImportError, OSError):
   nlp = None
   print("Warning: spaCy not available. Text preprocessing will be limited.")

def preprocess(text):
   if nlp is None:
       return text.lower().strip()
   doc = nlp(text)
   tokens = [token.lemma_.lower() for token in doc if not token.is_punct and not token.is_space]
   print(tokens)
   return " ".join(tokens)




client = OpenAI(api_key=api_key)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserInput(BaseModel):
   message: str
   sessionId: str


@app.get("/")
async def root():
   return {"message": "Hello, Socratic AI!"}


@app.post("/chat")
async def chat(input: UserInput):
   try:
       processedText = preprocess(input.message)
       histories[input.sessionId].append({"role": "user", "content" : processedText})
       output = client.chat.completions.create(
           model="gpt-4o-mini",
           messages=histories[input.sessionId]
       )
       histories[input.sessionId].append(output.choices[0].message)
       return {"response" : output.choices[0].message.content, "sessionId": input.sessionId}
   except OpenAIError as e:
       print(f"OpenAI API Error : {e}")
       return {"error" : "There seems to be an error with the OpenAI API. Please try again later"}