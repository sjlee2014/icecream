function ProductGrid({ products }) {
  if (!products || products.length === 0) {
    return (
      <div className="loading">
        <p>상품이 없습니다. 스크래핑을 실행해주세요.</p>
      </div>
    );
  }

  const formatPrice = (price) => {
    if (!price) return 'N/A';
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
    }).format(price);
  };

  return (
    <div className="products-grid">
      {products.map((product) => (
        <div key={product.id} className="product-card">
          <img
            src={product.image_url || '/placeholder.png'}
            alt={product.name}
            className="product-image"
            onError={(e) => {
              e.target.src = 'https://via.placeholder.com/250x200?text=No+Image';
            }}
          />
          <div className="product-info">
            <div className="product-name">{product.name}</div>
            <div className="product-price">{formatPrice(product.price)}</div>
            {product.discount_rate && (
              <div style={{ color: '#f44336', fontSize: '0.9rem' }}>
                {product.discount_rate}% 할인
              </div>
            )}
            <div className="product-badges">
              {product.is_new && <span className="badge badge-new">NEW</span>}
              {product.is_best && <span className="badge badge-best">BEST</span>}
              {product.is_sale && <span className="badge badge-sale">SALE</span>}
            </div>
            {product.rating > 0 && (
              <div style={{ marginTop: '0.5rem', color: '#666', fontSize: '0.85rem' }}>
                ⭐ {product.rating.toFixed(1)} ({product.review_count} 리뷰)
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ProductGrid;
