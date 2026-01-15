const CONFIG = {
  API_ENDPOINT: 'https://signalgeniusai-production.up.railway.app/api/v1/lab/market-reference',
  REFRESH_INTERVAL: 30000, // 30 seconds
  SYMBOL: 'EURUSD',
  TIMEFRAME: 'M15'
};

let refreshTimer = null;
let lastUpdateTime = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
  console.log('🚀 Signal Genius AI - Initializing...');
  initTheme();
  loadSignal();
  startAutoRefresh();
  updateRefreshIndicator();
});

// Theme Management
function initTheme() {
  const themeToggle = document.getElementById('theme-toggle');
  const body = document.body;
  const themeIcon = themeToggle.querySelector('.theme-icon');

  // Check saved theme
  const savedTheme = localStorage.getItem('theme') || 'dark';
  body.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme, themeIcon);

  themeToggle.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme, themeIcon);
  });
}

function updateThemeIcon(theme, iconElement) {
  iconElement.textContent = theme === 'dark' ? '🌙' : '☀️';
}

// Load signal data with Snapshot-First Strategy
async function loadSignal() {
  // 1️⃣ Render Cached Snapshot IMMEDIATELY
  const cached = localStorage.getItem('latest_signal');
  if (cached) {
    console.log('⚡ Rendered cached snapshot');
    renderSignal(JSON.parse(cached), true); // true = isCached
  } else {
    renderWaitingState();
  }

  // 2️⃣ Fetch Fresh Data in Background
  try {
    const signal = await fetchSignalData();

    if (signal) {
      // 3️⃣ Update UI with fresh data if valid
      if (signal.confidence >= 95) {
        renderSignal(signal, false); // false = isLive
        localStorage.setItem('latest_signal', JSON.stringify(signal));
      } else {
        // If live signal is low confidence but we have a cache, 
        // we might want to keep the cache or show waiting state.
        // For now, let's respect the "Scanning" state if confidence drops.
        renderWaitingState();
      }
    }
  } catch (error) {
    console.error('Background fetch failed:', error);
    // If fetch fails, we just keep showing the cached snapshot if it exists.
    // Optionally, we could show a subtle "Offline - Using Snapshot" toast here.
  }
}

// Fetch signal data from Railway API
async function fetchSignalData() {
  try {
    const response = await fetch(`${CONFIG.API_ENDPOINT}?symbol=${CONFIG.SYMBOL}&tf=${CONFIG.TIMEFRAME}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (data.message) {
      return null;
    }

    return data;
  } catch (error) {
    console.warn('API call failed, falling back to mock or cache:', error);
    // Fallback to mock data ONLY if enabled/needed for demo
    // return getMockSignal(); 
    return null;
  }
}

// Render signal card
function renderSignal(signal, isCached = false) {
  const container = document.getElementById('signal-container');
  const directionClass = signal.direction.toLowerCase();

  // UX Copy Definitions
  const statusBadge = isCached
    ? `<span class="status-badge cached" style="background: rgba(255, 193, 7, 0.1); color: #ffc107; padding: 4px 12px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; border: 1px solid rgba(255, 193, 7, 0.2);">⚡ AI SNAPSHOT LOADED</span>`
    : `<span class="status-badge live" style="background: rgba(16, 185, 129, 0.1); color: #10b981; padding: 4px 12px; border-radius: 99px; font-size: 0.75rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.2);">🟢 LIVE UPDATE</span>`;

  const html = `
    <div class="bento-card signal-card animate-in">
      <div class="signal-header">
        <div>
          <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 8px;">
            <h2 class="asset-name" style="margin-bottom: 0;">${signal.asset}</h2>
            ${statusBadge}
          </div>
          <div class="detail-label">
            ⏳ Timeframe: <strong>${signal.timeframe}</strong> | 🌍 ${signal.session}
          </div>
        </div>
        <div class="direction-badge ${directionClass}">
          ${signal.direction_icon} ${signal.direction}
        </div>
      </div>
      
      <div class="signal-details">
        <div class="detail-group">
          <div class="detail-label">💰 Price Levels</div>
          <div class="price-levels">
            <div class="price-item">
              <span class="price-label">Entry Zone:</span>
              <span class="price-value">${signal.price_levels.entry_zone[0]} – ${signal.price_levels.entry_zone[1]}</span>
            </div>
            <div class="price-item">
              <span class="price-label">Take Profit:</span>
              <span class="price-value" style="color: var(--accent-green)">${signal.price_levels.take_profit}</span>
            </div>
            <div class="price-item">
              <span class="price-label">Stop Loss:</span>
              <span class="price-value" style="color: #ff4444">${signal.price_levels.stop_loss}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-group">
          <div class="detail-label">📏 Trade Details</div>
          <div class="price-levels">
            <div class="price-item">
              <span class="price-label">Target:</span>
              <span class="price-value">+${signal.trade_details.target_pips} pips</span>
            </div>
            <div class="price-item">
              <span class="price-label">Risk–Reward:</span>
              <span class="price-value">${signal.trade_details.risk_reward}</span>
            </div>
            <div class="price-item">
              <span class="price-label">Suggested Risk:</span>
              <span class="price-value">${signal.trade_details.suggested_risk}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-group">
          <div class="detail-label">🕒 Trade Info</div>
          <div class="price-levels">
            <div class="price-item">
              <span class="price-label">Type:</span>
              <span class="price-value">${signal.trade_type}</span>
            </div>
            <div class="price-item">
              <span class="price-label">Posted:</span>
              <span class="price-value">${formatDateTime(signal.posted_at_utc)}</span>
            </div>
            <div class="price-item">
              <span class="price-label">AI Confidence:</span>
              <span class="confidence-badge">⭐ ${signal.confidence}%</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="expiry-rules">
        <h4>⏳ Auto-Expiry Rules</h4>
        <ul>
          <li>Signal is valid for this session only</li>
          <li>Expires at New York close or if TP or SL is hit</li>
          <li>Do not enter if price has already moved significantly beyond the entry zone</li>
        </ul>
      </div>
      
      <div style="text-align: center; margin-top: var(--spacing-md); padding-top: var(--spacing-md); border-top: 1px solid var(--border-color);">
        <small style="color: var(--text-secondary);">⚠️ ${signal.disclaimer}</small>
      </div>
    </div>
  `;

  container.innerHTML = html;
}

// Render waiting state
function renderWaitingState() {
  const container = document.getElementById('signal-container');

  const html = `
    <div class="bento-card signal-card animate-in">
      <div class="waiting-state">
        <div class="waiting-icon" style="color: var(--primary-cyan)">🎯</div>
        <h3 class="waiting-title" style="font-weight: 800; color: var(--text-primary);">Scanning Market...</h3>
        <p class="waiting-description" style="color: var(--text-secondary); font-weight: 500;">
          Signal Genius AI is analyzing EUR/USD market liquidity and momentum.
          <br><br>
          <span style="color: var(--primary-cyan); font-weight: 700;">Wait for 95% + Confidence.</span>
        </p>
      </div>
    </div>
  `;

  container.innerHTML = html;
}

// Format date time
function formatDateTime(isoString) {
  const date = new Date(isoString);
  const options = {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  };
  return date.toLocaleString('en-US', options) + ' UTC';
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    loadSignal,
    getMockSignal,
    formatDateTime
  };
}
