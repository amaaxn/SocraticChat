# SocraticChat

This project is a simple web application that engages users in Socratic Dialogue. It is powered by OpenAI's GPT-4 and built with a React frontend and FastAPI backend.

## Features

* Instructive chatbot engaging in Socratic Dialogue
* Basic NLP preprocessing using SpaCy
* Session-based chat history for multiple simultaneous conversations
* Deployed Frontend on Vercel and Backend on Render/Heroku

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/amaaxn/SocraticChat.git
cd SocraticChat
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

#### Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

#### Run the backend server:

```bash
uvicorn main:app --reload --port 8000
```

### 3. Set up the frontend (new terminal is needed)

```bash
cd ../frontend
npm install
```

#### Run the frontend server:

```bash
npm run dev
```

## Usage

Once both frontend and backend are running, navigate to http://localhost:5173 in your browser.

Type a message into the chat box to begin a Socratic conversation.

## Notes

* Make sure the backend is running before interacting with the frontend.
* API errors will appear in the browser console for debugging.
