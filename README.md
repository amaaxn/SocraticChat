# SocraticChat

An AI-powered application that integrates with GPT-4 to simulate Socratic dialogue. The application uses NLP preprocessing and provides a clean, intuitive web interface for engaging in thoughtful conversations.

## Overview

SocraticChat helps users think critically by asking probing questions rather than providing direct answers. Built with Python, FastAPI, and React, it demonstrates integration with advanced LLM APIs and modern web development practices.

## Core Features

- **LLM Integration**: Powered by OpenAI's GPT-4 API
- **NLP Preprocessing**: Tokenization and lemmatization using spaCy
- **Error Handling**: Comprehensive handling for API rate limits and errors
- **Modern UI**: Clean, responsive React frontend
- **Session Management**: Maintains conversation context

## Tech Stack

**Backend:**
- Python 3.8+
- FastAPI
- OpenAI API (GPT-4)
- spaCy (NLP processing)

**Frontend:**
- React 18
- Vite

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd SocraticChat
```

### Step 2: Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=your_api_key_here
```

### Step 3: Frontend Setup

```bash
cd frontend
npm install
```

### Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Open your browser and navigate to `http://localhost:5173`

## How It Works

1. **User Input**: User types a message in the web interface
2. **NLP Preprocessing**: Backend processes text using spaCy (tokenization, lemmatization, stop word removal)
3. **AI Response**: GPT-4 generates a Socratic-style response with thoughtful questions
4. **Context Maintenance**: Conversation history is maintained for coherent dialogue

## API Endpoints

- `POST /chat` - Send a message and receive a Socratic response
- `GET /health` - Check API health status
- `GET /` - API information

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set root directory to `frontend`
3. Build command: `npm install && npm run build`
4. Output directory: `dist`
5. Add environment variable: `VITE_API_URL=your_backend_url`

### Backend (Render/Heroku)

**Render:**
- Build command: `cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- Start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- Add environment variable: `OPENAI_API_KEY=your_key`

**Heroku:**
- The `Procfile` and `runtime.txt` are already configured
- Deploy using Heroku CLI or GitHub integration
- Set `OPENAI_API_KEY` in Heroku config vars

## Project Structure

```
SocraticChat/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Heroku deployment config
│   └── runtime.txt         # Python version
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Application styles
│   │   └── main.jsx        # React entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Error Handling

The application handles:
- **Rate Limits**: Returns 429 status with user-friendly message
- **Authentication Errors**: Returns 401 status for invalid API keys
- **API Errors**: Catches and logs OpenAI API errors
- **Network Issues**: Graceful error messages in the UI

## Notes

- Session data is stored in memory (not persistent across server restarts)
- The spaCy model (`en_core_web_sm`) must be downloaded before running
- Always start the backend server before the frontend

## License

This project is for educational purposes.
