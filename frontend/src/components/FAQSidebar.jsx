import { useState, useEffect } from 'react';
import { faqApi } from '../api/chatApi';

function FAQSidebar({ onFAQClick }) {
  const [faqs, setFaqs] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCategories();
    loadFAQs();
  }, []);

  useEffect(() => {
    loadFAQs(selectedCategory);
  }, [selectedCategory]);

  const loadCategories = async () => {
    try {
      const response = await faqApi.getCategories();
      setCategories(response.data);
    } catch (error) {
      console.error('카테고리 로딩 오류:', error);
    }
  };

  const loadFAQs = async (category = null) => {
    setLoading(true);
    try {
      const response = await faqApi.getAll(category);
      setFaqs(response.data);
    } catch (error) {
      console.error('FAQ 로딩 오류:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFAQClick = (faq) => {
    if (onFAQClick) {
      onFAQClick(faq.question);
    }
  };

  return (
    <div className="sidebar">
      <h3>자주 묻는 질문</h3>

      {categories.length > 0 && (
        <div className="faq-categories">
          <button
            className={`category-btn ${!selectedCategory ? 'active' : ''}`}
            onClick={() => setSelectedCategory(null)}
          >
            전체
          </button>
          {categories.map((category) => (
            <button
              key={category}
              className={`category-btn ${selectedCategory === category ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category)}
            >
              {category}
            </button>
          ))}
        </div>
      )}

      {loading ? (
        <div className="loading">
          <div className="loading-spinner"></div>
          <p>FAQ를 불러오는 중...</p>
        </div>
      ) : (
        <div className="faq-list">
          {faqs.length === 0 ? (
            <p style={{ textAlign: 'center', color: '#999', padding: '2rem 0' }}>
              FAQ가 없습니다
            </p>
          ) : (
            faqs.map((faq) => (
              <div
                key={faq.id}
                className="faq-item"
                onClick={() => handleFAQClick(faq)}
              >
                <div className="faq-question">{faq.question}</div>
                <div className="faq-answer">{faq.answer}</div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default FAQSidebar;
