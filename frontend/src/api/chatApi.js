import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Chat API
export const chatApi = {
  startConversation: () => apiClient.post('/chat/start'),
  sendMessage: (sessionId, content) =>
    apiClient.post('/chat/message', { session_id: sessionId, content }),
  getHistory: (sessionId) => apiClient.get(`/chat/history/${sessionId}`),
  getConversations: (limit = 50, status = null) =>
    apiClient.get('/chat/conversations', { params: { limit, status } }),
  closeConversation: (sessionId) => apiClient.post(`/chat/close/${sessionId}`),
};

// FAQ API
export const faqApi = {
  getAll: (category = null) => apiClient.get('/faq/', { params: { category } }),
  getCategories: () => apiClient.get('/faq/categories'),
  getById: (id) => apiClient.get(`/faq/${id}`),
  markHelpful: (id) => apiClient.post(`/faq/${id}/helpful`),
  search: (keyword) => apiClient.get(`/faq/search/${keyword}`),
};

export default apiClient;
