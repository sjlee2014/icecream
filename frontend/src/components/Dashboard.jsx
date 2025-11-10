import { useState, useEffect } from 'react';
import { productsApi, scraperApi } from '../api/client';
import ProductGrid from './ProductGrid';
import StatsOverview from './StatsOverview';
import ScraperControl from './ScraperControl';

function Dashboard() {
  const [activeTab, setActiveTab] = useState('trending');
  const [products, setProducts] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [scraperStatus, setScraperStatus] = useState(null);

  useEffect(() => {
    loadData();
    loadScraperStatus();

    // Refresh scraper status every 10 seconds
    const interval = setInterval(loadScraperStatus, 10000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    loadProducts();
  }, [activeTab]);

  const loadData = async () => {
    try {
      const statsResponse = await productsApi.getStats();
      setStats(statsResponse.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const loadProducts = async () => {
    setLoading(true);
    try {
      let response;
      switch (activeTab) {
        case 'trending':
          response = await productsApi.getTrending();
          break;
        case 'best-sellers':
          response = await productsApi.getBestSellers();
          break;
        case 'new-arrivals':
          response = await productsApi.getNewArrivals();
          break;
        case 'on-sale':
          response = await productsApi.getOnSale();
          break;
        default:
          response = await productsApi.getAll({ limit: 20 });
      }
      setProducts(response.data);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadScraperStatus = async () => {
    try {
      const response = await scraperApi.getStatus();
      setScraperStatus(response.data);
    } catch (error) {
      console.error('Error loading scraper status:', error);
    }
  };

  const handleScrape = async () => {
    try {
      await scraperApi.run();
      alert('스크래핑이 시작되었습니다!');
      loadScraperStatus();
    } catch (error) {
      console.error('Error starting scraper:', error);
      alert('스크래핑 시작 중 오류가 발생했습니다.');
    }
  };

  const tabs = [
    { id: 'trending', label: '트렌딩 상품' },
    { id: 'best-sellers', label: '베스트셀러' },
    { id: 'new-arrivals', label: '신상품' },
    { id: 'on-sale', label: '세일 상품' },
  ];

  return (
    <div className="app">
      <div className="header">
        <h1>🍦 아이스크림몰 상품 분석 대시보드</h1>
        <p>i-screammall.co.kr 실시간 상품 트렌드 분석</p>
      </div>

      <div className="container">
        <ScraperControl
          status={scraperStatus}
          onScrape={handleScrape}
        />

        {stats && <StatsOverview stats={stats} />}

        <div className="section">
          <div className="tabs">
            {tabs.map(tab => (
              <button
                key={tab.id}
                className={`tab ${activeTab === tab.id ? 'active' : ''}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {loading ? (
            <div className="loading">
              <div className="loading-spinner"></div>
              <p>상품 정보를 불러오는 중...</p>
            </div>
          ) : (
            <ProductGrid products={products} />
          )}
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
