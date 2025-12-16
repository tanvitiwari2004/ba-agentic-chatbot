import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { BALogo, Speedmarque } from './BALogo';
import './App.css';

function App() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: "Welcome to **British Airways**. I am your personal concierge. How may I assist you with your journey today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const messagesEndRef = useRef(null);

  const API_URL = 'http://localhost:8000';

  const SUGGESTIONS = [
    "What is the baggage allowance?",
    "Liquid restrictions for hand luggage",
    "Special assistance requests",
    "Traveling with pets"
  ];

  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackStep, setFeedbackStep] = useState('rating'); // 'rating', 'reason', 'thanks'
  const [isSatisfied, setIsSatisfied] = useState(null);

  useEffect(() => {
    if (messages.length > 1) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const sendMessage = async (text = input) => {
    if (!text.trim() || loading) return;

    const userMessage = {
      role: 'user',
      content: text,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: text,
          conversation_id: conversationId
        })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      setConversationId(data.conversation_id);

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response,
        confidence: data.confidence,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'I apologize, but I am momentarily unable to access the service. Please verify your connection.',
        error: true,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleEndChat = () => {
    setShowFeedback(true);
    setFeedbackStep('rating');
  };

  const submitFeedback = async (satisfied, reason = null) => {
    try {
      // Get the last interaction to send with feedback
      const lastUserMsg = messages.filter(m => m.role === 'user').pop();
      const lastAssistantMsg = messages.filter(m => m.role === 'assistant').pop();

      await fetch(`${API_URL}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          satisfied,
          reason,
          query: lastUserMsg?.content,
          response: lastAssistantMsg?.content
        })
      });
    } catch (err) {
      console.error("Failed to submit feedback", err);
    }
  };

  const handleRating = (satisfied) => {
    setIsSatisfied(satisfied);
    if (satisfied) {
      submitFeedback(true);
      setFeedbackStep('thanks');
      setTimeout(closeFeedback, 2000);
    } else {
      setFeedbackStep('reason');
    }
  };

  const submitReason = (reason) => {
    submitFeedback(false, reason);
    setFeedbackStep('thanks');
    setTimeout(closeFeedback, 2000);
  };

  const closeFeedback = () => {
    setShowFeedback(false);
    setMessages([{ // Reset chat
      role: 'assistant',
      content: "Welcome to **British Airways**. I am your personal concierge. How may I assist you with your journey today?",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }]);
    setConversationId(null);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="header-content">
          <div className="logo-container">
            <BALogo className="ba-logo-full" />
          </div>
          <div className="header-info">
            <span className="status">
              <span className="status-dot"></span>
              Concierge Online
            </span>
            <button className="end-chat-btn" onClick={handleEndChat}>
              End Chat
            </button>
          </div>
        </div>
      </header>

      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-wrapper">
                <div className="message-content">
                  <div className="message-text">
                    {msg.role === 'assistant' ? (
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    ) : (
                      msg.content
                    )}
                  </div>
                </div>
                <div className="message-meta">
                  {msg.role === 'assistant' && <Speedmarque />}
                  <span className="timestamp">{msg.timestamp}</span>
                </div>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message assistant">
              <div className="message-wrapper">
                <div className="message-content">
                  <div className="message-text typing-bubble">
                    <div className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                    <span className="typing-text">Concierge is thinking...</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {messages.length === 1 && !loading && (
            <div className="suggestions">
              <p className="suggestions-title">How can we help you travel?</p>
              <div className="suggestions-grid">
                {SUGGESTIONS.map((s, i) => (
                  <button key={i} onClick={() => sendMessage(s)} className="suggestion-chip">
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        <div className="input-form">
          <div className="input-wrapper">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="Type your request here..."
              rows="1"
              disabled={loading}
            />
            <button onClick={() => sendMessage()} disabled={loading || !input.trim()}>
              <span className="send-icon">➤</span>
            </button>
          </div>
          <div className="input-hint">
            British Airways Digital Concierge • Powered by GPT-4o
          </div>
        </div>
      </div>

      {showFeedback && (
        <div className="feedback-overlay">
          <div className="feedback-card">
            {feedbackStep === 'rating' && (
              <>
                <h3>How was your experience?</h3>
                <div className="feedback-actions">
                  <button className="feedback-btn good" onClick={() => handleRating(true)}>
                    Satisfied
                  </button>
                  <button className="feedback-btn bad" onClick={() => handleRating(false)}>
                    Not Satisfied
                  </button>
                </div>
              </>
            )}

            {feedbackStep === 'reason' && (
              <>
                <h3>We're sorry to hear that. What went wrong?</h3>
                <div className="feedback-reasons">
                  {['Inaccurate Information', 'Slow Response', 'Did not understand', 'Other'].map(r => (
                    <button key={r} onClick={() => submitReason(r)} className="reason-chip">
                      {r}
                    </button>
                  ))}
                </div>
              </>
            )}

            {feedbackStep === 'thanks' && (
              <div className="feedback-thanks">
                <h3>Thank you for your feedback.</h3>
                <p>We look forward to serving you again.</p>
              </div>
            )}

            {feedbackStep !== 'thanks' && (
              <button className="feedback-close" onClick={() => setShowFeedback(false)}>Close</button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;