import './App.css';
import ChatBox from './components/ChatBox';
import FAQSidebar from './components/FAQSidebar';

function App() {
  const handleFAQClick = (question) => {
    // FAQ 클릭 시 챗봇에 질문 전달 (선택사항)
    console.log('FAQ 클릭:', question);
  };

  return (
    <div className="app">
      <div className="header">
        <h1>🍦 아이스크림몰 고객 상담</h1>
        <p>무엇을 도와드릴까요? 궁금하신 점을 편하게 물어보세요!</p>
      </div>

      <div className="chat-container">
        <ChatBox />
        <FAQSidebar onFAQClick={handleFAQClick} />
      </div>
    </div>
  );
}

export default App;
