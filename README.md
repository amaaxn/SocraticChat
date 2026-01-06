# SocraticChat

A simple AI-powered web application that engages users in Socratic dialogue using advanced LLM APIs. Built with FastAPI backend and React frontend.

## Features

- 🤔 **Socratic Dialogue**: Engage in thoughtful conversations with an AI that asks probing questions
- 🧠 **NLP Preprocessing**: Tokenization and lemmatization using spaCy
- 💬 **Session Management**: Maintain conversation context across messages
- ⚡ **Error Handling**: Robust error handling for API rate limits and errors
- 🎨 **Clean UI/UX**: Modern, intuitive interface with smooth animations
- 🚀 **Easy Deployment**: Ready for deployment on Vercel (frontend) and Render/Heroku (backend)

## Tech Stack

- **Backend**: Python, FastAPI, OpenAI GPT-4, spaCy
- **Frontend**: React, Vite
- **Deployment**: Vercel (frontend), Render/Heroku (backend)

## Installation

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download spaCy language model:
```bash
python -m spacy download en_core_web_sm
```

5. Create a `.env` file in the backend directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

6. Run the backend server:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory (in a new terminal):
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (optional, defaults to localhost):
```bash
VITE_API_URL=http://localhost:8000
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Usage

1. Start the backend server (see Backend Setup)
2. Start the frontend server (see Frontend Setup)
3. Open your browser and navigate to `http://localhost:5173`
4. Type a message to begin a Socratic conversation
5. The AI will respond with thoughtful questions to guide your thinking

## API Endpoints

### `POST /chat`
Send a message and receive a Socratic response.

**Request:**
```json
{
  "message": "What is justice?",
  "session_id": "optional_session_id"
}
```

**Response:**
```json
{
  "response": "That's an interesting question. What do you think justice means to you?",
  "session_id": "session_1234567890",
  "processed_input": "justice"
}
```

### `GET /health`
Check API health status.

### `GET /sessions/{session_id}`
Retrieve conversation history for a session.

### `DELETE /sessions/{session_id}`
Clear conversation history for a session.

## Deployment

### Frontend (Vercel)

1. Push your code to GitHub
2. Import your repository on Vercel
3. Set build command: `cd frontend && npm install && npm run build`
4. Set output directory: `frontend/dist`
5. Add environment variable: `VITE_API_URL=your_backend_url`
6. Deploy

### Backend (Render/Heroku)

#### Render:
1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Set build command: `cd backend && pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Set start command: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENAI_API_KEY=your_key`
6. Deploy

#### Heroku:
1. Create a `Procfile` in the backend directory:
```
web: cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. Create a `runtime.txt` in the backend directory:
```
python-3.11.0
```

3. Deploy using Heroku CLI or GitHub integration

## Error Handling

The application handles various error scenarios:
- **Rate Limit Errors (429)**: User-friendly message when API rate limit is exceeded
- **Authentication Errors (401)**: Clear message when API key is invalid
- **API Errors (500)**: Graceful handling of unexpected API errors
- **Network Errors**: Frontend displays error messages for connection issues

## Project Structure

```
SocraticChat/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment variables template
│   └── .gitignore
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Styles
│   │   ├── main.jsx        # Entry point
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .gitignore
├── README.md
└── .gitignore
```

## Notes

- Make sure the backend is running before interacting with the frontend
- API errors will appear in the browser console for debugging
- Session data is stored in memory (use a database for production)
- The spaCy model must be downloaded before running the backend

## License

This project is open source and available for educational purposes.

## Contact

For questions or issues, please open an issue on GitHub.
