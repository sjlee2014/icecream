import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Products API
export const productsApi = {
  getAll: (params) => apiClient.get('/products/', { params }),
  getStats: () => apiClient.get('/products/stats'),
  getTrending: (limit = 20) => apiClient.get('/products/trending', { params: { limit } }),
  getBestSellers: (limit = 20) => apiClient.get('/products/best-sellers', { params: { limit } }),
  getNewArrivals: (limit = 20) => apiClient.get('/products/new-arrivals', { params: { limit } }),
  getOnSale: (limit = 20) => apiClient.get('/products/on-sale', { params: { limit } }),
  getById: (id) => apiClient.get(`/products/${id}`),
};

// Scraper API
export const scraperApi = {
  run: () => apiClient.post('/scraper/run'),
  getLogs: (limit = 20) => apiClient.get('/scraper/logs', { params: { limit } }),
  getStatus: () => apiClient.get('/scraper/status'),
};

export default apiClient;
