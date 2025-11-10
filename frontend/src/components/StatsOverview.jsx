function StatsOverview({ stats }) {
  const formatNumber = (num) => {
    return new Intl.NumberFormat('ko-KR').format(num);
  };

  const formatPrice = (price) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      maximumFractionDigits: 0,
    }).format(price);
  };

  return (
    <div className="stats-grid">
      <div className="stat-card">
        <h3>전체 상품</h3>
        <div className="value">{formatNumber(stats.total_products)}</div>
      </div>
      <div className="stat-card">
        <h3>판매중 상품</h3>
        <div className="value">{formatNumber(stats.available_products)}</div>
      </div>
      <div className="stat-card">
        <h3>신상품</h3>
        <div className="value">{formatNumber(stats.new_products)}</div>
      </div>
      <div className="stat-card">
        <h3>베스트 상품</h3>
        <div className="value">{formatNumber(stats.best_products)}</div>
      </div>
      <div className="stat-card">
        <h3>세일 상품</h3>
        <div className="value">{formatNumber(stats.sale_products)}</div>
      </div>
      <div className="stat-card">
        <h3>평균 가격</h3>
        <div className="value" style={{ fontSize: '1.5rem' }}>
          {formatPrice(stats.avg_price)}
        </div>
      </div>
      <div className="stat-card">
        <h3>평균 할인율</h3>
        <div className="value">{stats.avg_discount_rate.toFixed(1)}%</div>
      </div>
      <div className="stat-card">
        <h3>카테고리</h3>
        <div className="value">{stats.categories.length}</div>
      </div>
    </div>
  );
}

export default StatsOverview;
