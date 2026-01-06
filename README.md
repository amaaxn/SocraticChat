# SocraticChat

An AI-powered conversational application that uses the Socratic method to engage users in deep, thoughtful dialogue. Built with modern web technologies to create an intuitive and engaging learning experience.

## What is SocraticChat?

SocraticChat is designed to help you think critically by asking probing questions rather than providing direct answers. The application leverages OpenAI's GPT-4 to simulate a Socratic teacher, guiding conversations that encourage self-discovery and deeper understanding.

## Key Features

- **Intelligent Dialogue**: Powered by GPT-4 for natural, context-aware conversations
- **NLP Processing**: Uses spaCy for text preprocessing, including tokenization and lemmatization
- **Session Management**: Maintains conversation context across multiple messages
- **Error Resilience**: Comprehensive error handling for API rate limits and connection issues
- **Modern UI**: Clean, responsive interface built with React and Vite
- **Production Ready**: Configured for easy deployment on popular hosting platforms

## Tech Stack

**Backend:**
- Python 3.11
- FastAPI (async web framework)
- OpenAI API (GPT-4)
- spaCy (NLP processing)

**Frontend:**
- React 18
- Vite (build tool)
- Modern CSS with gradient designs

## Getting Started

### Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- Node.js 16 or higher installed
- An OpenAI API key ([get one here](https://platform.openai.com/api-keys))

### Installation Steps

1. **Clone this repository**
   ```bash
   git clone https://github.com/amaaxn/SocraticChat.git
   cd SocraticChat
   ```

2. **Backend Setup**
   
   Navigate to the backend directory and set up the Python environment:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
   
   Create a `.env` file in the `backend` directory:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```
   
   Start the backend server:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

3. **Frontend Setup**
   
   Open a new terminal and navigate to the frontend directory:
   ```bash
   cd frontend
   npm install
   ```
   
   (Optional) Create a `.env` file if your backend is running on a different URL:
   ```env
   VITE_API_URL=http://localhost:8000
   ```
   
   Start the development server:
   ```bash
   npm run dev
   ```

4. **Start Chatting!**
   
   Open your browser and go to `http://localhost:5173`. Type your first message to begin a Socratic dialogue.

## How It Works

1. **User Input**: You type a question or statement
2. **NLP Processing**: The backend preprocesses your text using spaCy (tokenization, lemmatization)
3. **AI Response**: GPT-4 generates a Socratic-style response that asks thoughtful questions
4. **Context Maintenance**: The conversation history is maintained for coherent dialogue

## API Endpoints

- `POST /chat` - Send a message and receive a Socratic response
- `GET /health` - Check API health status
- `GET /sessions/{session_id}` - Retrieve conversation history
- `DELETE /sessions/{session_id}` - Clear conversation history

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set the root directory to `frontend`
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
│   ├── main.py              # FastAPI application and API endpoints
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment variable template
│   ├── Procfile            # Heroku deployment config
│   └── runtime.txt         # Python version for Heroku
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   ├── App.css         # Application styles
│   │   ├── main.jsx        # React entry point
│   │   └── index.css       # Global styles
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
├── README.md
└── .gitignore
```

## Important Notes

- Always start the backend server before the frontend
- The spaCy model (`en_core_web_sm`) must be downloaded before running the backend
- Session data is stored in memory (not persistent across server restarts)
- Check browser console for debugging information if issues arise

## License

This project is open source and available for educational purposes.

---

Built with ❤️ for thoughtful conversations
