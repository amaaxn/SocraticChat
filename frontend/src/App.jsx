import { useState, useRef, useEffect } from 'react'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [sessionId, setSessionId] = useState(null)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const userMessage = input.trim()
    setInput('')
    setError(null)

    const newUserMessage = { role: 'user', content: userMessage }
    setMessages(prev => [...prev, newUserMessage])
    setLoading(true)

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          sessionId: sessionId,
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to get response')
      }

      const data = await response.json()
      
      if (!sessionId && data.sessionId) {
        setSessionId(data.sessionId)
      }

      setMessages(prev => [...prev, { role: 'assistant', content: data.response }])
    } catch (err) {
      setError(err.message)
      setMessages(prev => prev.slice(0, -1))
    } finally {
      setLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
    setSessionId(null)
    setError(null)
    // Session cleanup handled by backend
  }

  return (
    <div className="app">
      <header className="header">
        <h1>🤔 SocraticChat</h1>
        <p className="subtitle">Engage in thoughtful dialogue</p>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 ? (
            <div className="welcome-message">
              <p>Welcome to SocraticChat!</p>
              <p>I'm here to help you think through your ideas by asking thoughtful questions.</p>
              <p>What would you like to explore today?</p>
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="message assistant">
              <div className="message-content">
                <span className="typing-indicator">Thinking...</span>
              </div>
            </div>
          )}
          {error && (
            <div className="error-message">
              <p>⚠️ {error}</p>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={loading}
            className="message-input"
          />
          <button type="submit" disabled={loading || !input.trim()} className="send-button">
            Send
          </button>
          {messages.length > 0 && (
            <button type="button" onClick={clearChat} className="clear-button">
              Clear
            </button>
          )}
        </form>
      </div>
    </div>
  )
}

export default App
