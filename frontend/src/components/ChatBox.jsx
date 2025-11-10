import { useState, useEffect, useRef } from 'react';
import { chatApi } from '../api/chatApi';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [quickReplies, setQuickReplies] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    startConversation();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const startConversation = async () => {
    try {
      const response = await chatApi.startConversation();
      setSessionId(response.data.session_id);
      setQuickReplies(response.data.quick_replies || []);

      // 환영 메시지 표시
      setMessages([
        {
          id: 1,
          content: response.data.message || '안녕하세요! 무엇을 도와드릴까요?',
          sender_type: 'bot',
          created_at: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      console.error('대화 시작 오류:', error);
    }
  };

  const sendMessage = async () => {
    if (!inputText.trim() || !sessionId) return;

    const userMessage = {
      id: Date.now(),
      content: inputText,
      sender_type: 'customer',
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputText('');
    setIsTyping(true);

    try {
      const response = await chatApi.sendMessage(sessionId, inputText);

      setIsTyping(false);

      const botMessage = response.data.bot_message;
      setMessages((prev) => [...prev, botMessage]);

      setQuickReplies(response.data.quick_replies || []);
    } catch (error) {
      console.error('메시지 전송 오류:', error);
      setIsTyping(false);
    }
  };

  const handleQuickReply = (value) => {
    setInputText(value);
    setTimeout(() => sendMessage(), 100);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatTime = (dateString) => {
    return new Date(dateString).toLocaleTimeString('ko-KR', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="chat-box">
      <div className="chat-header">
        <h2>고객 상담</h2>
        <div className="chat-status">
          <span className="status-online">● 온라인</span> - 실시간 상담 가능
        </div>
      </div>

      <div className="messages">
        {messages.map((msg) => (
          <div key={msg.id} className={`message ${msg.sender_type}`}>
            <div className="message-avatar">
              {msg.sender_type === 'bot' ? '🤖' : '👤'}
            </div>
            <div className="message-content">
              <div className="message-bubble">{msg.content}</div>
              <div className="message-time">{formatTime(msg.created_at)}</div>
            </div>
          </div>
        ))}

        {isTyping && (
          <div className="message bot">
            <div className="message-avatar">🤖</div>
            <div className="message-content">
              <div className="message-bubble">
                <div className="typing-indicator">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {quickReplies.length > 0 && (
        <div className="quick-replies">
          {quickReplies.map((reply, index) => (
            <button
              key={index}
              className="quick-reply-btn"
              onClick={() => handleQuickReply(reply.value)}
            >
              {reply.label}
            </button>
          ))}
        </div>
      )}

      <div className="input-area">
        <input
          type="text"
          className="message-input"
          placeholder="메시지를 입력하세요..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
        />
        <button
          className="send-button"
          onClick={sendMessage}
          disabled={!inputText.trim()}
        >
          전송
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
