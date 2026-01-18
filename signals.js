export function renderRow(data) {
  const isBuy = data.direction === 'BUY';
  const directionClass = isBuy ? 'buy' : 'sell';

  // Format data
  const entry = data.entry || '0.00000';
  const tp = data.tp || '0.00000';
  const sl = data.sl || '0.00000';
  const confidence = data.confidence || 0;
  const time = new Date().toLocaleTimeString();

  const cardHtml = `
    <div class="bento-card signal-card animate-in">
      <div class="signal-header">
        <div class="asset-name">${data.asset || 'EUR/USD'}</div>
        <div class="direction-badge ${directionClass}">
          ${isBuy ? '▲' : '▼'} ${data.direction}
        </div>
      </div>

      <div class="signal-details">
        <!-- Confidence & Meta -->
        <div class="detail-group">
          <div class="detail-label">AI Confidence</div>
          <div class="confidence-badge">
             ⚡ ${confidence}%
          </div>
          
          <div style="margin-top: 1rem; display: flex; justify-content: space-between;">
            <div>
                <div class="detail-label">Timeframe</div>
                <div class="detail-value">${data.timeframe || 'M15'}</div>
            </div>
            <div>
                <div class="detail-label">Session</div>
                <div class="detail-value">London</div>
            </div>
          </div>
        </div>

        <!-- Levels -->
        <div class="detail-group">
          <div class="price-levels">
            <div class="price-item">
              <span class="price-label">ENTRY</span>
              <span class="price-value" style="color: var(--primary-cyan)">${entry}</span>
            </div>
            <div class="price-item">
              <span class="price-label">TAKE PROFIT</span>
              <span class="price-value" style="color: var(--accent-green)">${tp}</span>
            </div>
            <div class="price-item">
              <span class="price-label">STOP LOSS</span>
              <span class="price-value" style="color: #ff4444">${sl}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="expiry-rules">
        <h4>⚠️ Execution Rules</h4>
        <ul>
            <li><strong>Risk:</strong> Recommended 1% risk per trade.</li>
            <li><strong>Invalidation:</strong> Signal invalid if price hits SL or after 3 candles.</li>
            <li><strong>Generated:</strong> ${time}</li>
        </ul>
      </div>
    </div>
  `;

  return `<tr><td>${cardHtml}</td></tr>`;
}

export function renderStats(data) {
  return "";
}
