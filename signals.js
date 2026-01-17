/**
 * Signals Formatter - Product-Grade Card UI
 */

export function renderStats(stats) {
  if (!stats) return "";
  return `
    <div class="stat-item">
      <div class="label">Win Rate</div>
      <div class="val" style="color: var(--success)">${stats.win_rate}%</div>
    </div>
    <div class="stat-item">
      <div class="label">Pips</div>
      <div class="val" style="color: var(--primary-accent)">${stats.avg_pips > 0 ? '+' : ''}${stats.avg_pips}</div>
    </div>
    <div class="stat-item">
      <div class="label">Wins</div>
      <div class="val">${stats.win}</div>
    </div>
    <div class="stat-item">
      <div class="label">Losses</div>
      <div class="val">${stats.loss}</div>
    </div>
  `;
}

export function getConfidenceMeta(confidence) {
  if (confidence >= 75) {
    return {
      label: "STRONG",
      class: "confidence-75",
      color: "#16a34a",
      icon: "🟢",
      warning: null
    }
  }
  if (confidence >= 60) {
    return {
      label: "NORMAL",
      class: "confidence-60",
      color: "#2563eb",
      icon: "🔵",
      warning: "Trade with caution. Wait for confirmation."
    }
  }
  if (confidence >= 50) {
    return {
      label: "LOW",
      class: "confidence-50",
      color: "#ca8a04",
      icon: "🟡",
      warning: "Low probability setup. For reference only."
    }
  }
  return {
    label: "NO TRADE",
    class: "confidence-low",
    color: "#dc2626",
    icon: "🔴",
    warning: "Risky market conditions. No trade recommended."
  }
}

export function calcExpiryPercent(createdAt, expiryMinutes) {
  if (!createdAt || !expiryMinutes) return 0;
  const now = Date.now();
  const start = new Date(createdAt).getTime();
  const elapsed = (now - start) / 60000; // minutes
  return Math.min(100, Math.max(0, (elapsed / expiryMinutes) * 100));
}

export function renderCard(data) {
  if (!data || data.status !== "ok" || !data.payload) {
    return `<div class="signal-card error">⚠️ No valid signal data available</div>`;
  }

  const p = data.payload;
  const meta = getConfidenceMeta(p.confidence);
  const expiryPercent = calcExpiryPercent(p.generated_at, p.expiry?.minutes || 45);
  const isStabilizer = p.strategy === "Stabilizer" || p.signal_id?.includes("STAB");

  return `
    <div class="signal-card">
      <div class="signal-header">
        <h2 style="font-weight: 700; color: #fff; font-size: 20px;">${p.symbol}</h2>
        <span class="status-label">${isStabilizer ? 'STABILIZER' : 'CORE ENGINE'}</span>
      </div>

      <div class="signal-direction ${p.direction === 'BUY' ? 'buy' : 'sell'}" style="margin-top: 10px;">
        ${p.direction === 'BUY' ? '🟢 BUY' : '🔴 SELL'}
      </div>

      <div style="display: flex; gap: 8px; margin-bottom: 20px;">
        <div class="confidence-badge ${meta.class}" style="margin-bottom: 0; padding: 6px 12px; font-size: 12px;">
          ${meta.icon} ${p.confidence}% ${meta.label}
        </div>
        <div class="status-label" style="background: rgba(59, 130, 246, 0.1); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.2); padding: 6px 12px; font-size: 10px;">
          📅 TODAY'S SIGNAL (LIVE)
        </div>
      </div>

      ${meta.warning ? `<div class="warning">⚠️ ${meta.warning}</div>` : ""}

      <div class="detail-grid">
        <div class="detail-box">
          <label>Entry</label>
          <span>${p.entry}</span>
        </div>
        <div class="detail-box">
          <label>Timeframe</label>
          <span>${p.timeframe}</span>
        </div>
        <div class="detail-box">
          <label>Take Profit</label>
          <span class="success">${p.tp}</span>
        </div>
        <div class="detail-box">
          <label>Stop Loss</label>
          <span class="danger">${p.sl}</span>
        </div>
      </div>

      <div class="expiry-container">
        <div class="expiry-label">
          <span style="font-size: 11px;">VALIDITY</span>
          <span style="font-size: 11px;">EXTENDED WINDOW</span>
        </div>
        <div class="expiry-bar">
          <div class="expiry-progress" style="width: ${expiryPercent}%"></div>
        </div>
        <div style="text-align: center; font-size: 10px; color: var(--text-muted); margin-top: 12px; background: rgba(255,255,255,0.03); padding: 8px; border-radius: 10px;">
            Updated every 30s • Valid for current session
        </div>
      </div>

      <div class="signal-footer" style="margin-top: 20px; font-size: 10px; opacity: 0.6; display: flex; justify-content: space-between;">
        <span>ID: <b>${p.signal_id || 'N/A'}</b></span>
        <span>VOL: <b>0.12%</b></span>
      </div>
    </div>
  `;
}

