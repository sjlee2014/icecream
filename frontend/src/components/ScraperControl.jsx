function ScraperControl({ status, onScrape }) {
  if (!status) {
    return null;
  }

  const { is_running, current_job, last_scrape } = status;

  const getStatusBadge = () => {
    if (is_running) {
      return <span className="status-badge status-running">🔄 실행 중</span>;
    }
    if (last_scrape) {
      if (last_scrape.status === 'success') {
        return <span className="status-badge status-success">✅ 완료</span>;
      }
      if (last_scrape.status === 'failed') {
        return <span className="status-badge status-failed">❌ 실패</span>;
      }
    }
    return <span className="status-badge">대기 중</span>;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleString('ko-KR');
  };

  return (
    <div className="section">
      <div className="section-header">
        <h2>🔍 스크래퍼 제어</h2>
        <button
          className="button button-primary"
          onClick={onScrape}
          disabled={is_running}
        >
          {is_running ? '스크래핑 실행 중...' : '스크래핑 시작'}
        </button>
      </div>

      <div className="scraper-status">
        <div style={{ marginBottom: '1rem' }}>
          <strong>상태: </strong>
          {getStatusBadge()}
        </div>

        {last_scrape && (
          <div style={{ fontSize: '0.9rem', color: '#666' }}>
            <div>
              <strong>마지막 스크래핑:</strong> {formatDate(last_scrape.started_at)}
            </div>
            <div>
              <strong>수집된 상품:</strong> {last_scrape.products_scraped}개
              (신규: {last_scrape.products_new}, 업데이트: {last_scrape.products_updated})
            </div>
            {last_scrape.duration_seconds && (
              <div>
                <strong>소요 시간:</strong> {last_scrape.duration_seconds.toFixed(1)}초
              </div>
            )}
            {last_scrape.error_message && (
              <div style={{ color: '#f44336', marginTop: '0.5rem' }}>
                <strong>오류:</strong> {last_scrape.error_message}
              </div>
            )}
          </div>
        )}

        {is_running && current_job && (
          <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#856404' }}>
            현재 스크래핑 진행 중... 시작 시간: {formatDate(current_job.started_at)}
          </div>
        )}
      </div>
    </div>
  );
}

export default ScraperControl;
