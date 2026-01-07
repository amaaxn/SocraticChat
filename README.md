# SocraticChat

An AI-powered application that integrates with GPT-4 to simulate Socratic dialogue. The application uses NLP preprocessing and provides a clean, intuitive web interface for engaging in thoughtful conversations.

## Overview

SocraticChat helps users think critically by asking probing questions rather than providing direct answers. Built with Python, FastAPI, and React, it demonstrates integration with advanced LLM APIs and modern web development practices.

## Features

- **LLM Integration**: Powered by OpenAI's GPT-4o-mini API
- **NLP Preprocessing**: Tokenization and lemmatization using spaCy
- **Error Handling**: Comprehensive handling for API rate limits and errors
- **Modern UI**: Clean, responsive React frontend
- **Session Management**: Maintains conversation context

## Tech Stack

**Backend:**
- Python 3.12
- FastAPI
- OpenAI API (GPT-4o-mini)
- spaCy (NLP processing)

**Frontend:**
- React 18
- Vite

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Backend Setup

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

### Frontend Setup

```bash
cd frontend
npm install
```

### Running the Application

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

Open your browser and navigate to `http://localhost:5173`

## How It Works

1. User types a message in the web interface
2. Backend processes text using spaCy (tokenization, lemmatization)
3. GPT-4o-mini generates a Socratic-style response with thoughtful questions
4. Conversation history is maintained for coherent dialogue

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
5. Add environment variable: `VITE_API_URL=https://your-railway-backend-url.railway.app`

### Backend (Railway)

1. Connect your GitHub repository to Railway
2. Set root directory to `backend`
3. Railway will auto-detect Python and install dependencies
4. Add environment variable: `OPENAI_API_KEY=your_api_key`
5. Generate a public domain in Railway settings
6. The `Procfile` is already configured for deployment

## Project Structure

```
SocraticChat/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Railway deployment config
│   └── runtime.txt         # Python version
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Application styles
│   │   └── main.jsx        # React entry point
│   ├── package.json
│   ├── vercel.json         # Vercel deployment config
│   └── vite.config.js
└── README.md
```

## Error Handling

The application handles:
- **Rate Limits**: Returns user-friendly error messages
- **Authentication Errors**: Handles invalid API keys
- **API Errors**: Catches and handles OpenAI API errors
- **Network Issues**: Graceful error messages in the UI

## Notes

- Session data is stored in memory (not persistent across server restarts)
- The spaCy model (`en_core_web_sm`) must be downloaded before running
- Always start the backend server before the frontend

## License

This project is for educational purposes.
