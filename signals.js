export function getSignalStatus(signal) {
  const ageMin = (Date.now() - new Date(signal.timestamp)) / 60000;
  const validity = signal.validity || 90;
  const isLive = ageMin <= validity;
  return {
    isLive,
    text: isLive ? "LIVE" : "EXPIRED",
    class: isLive ? "live" : "expired",
    icon: isLive ? "🟢" : "🔴"
  };
}

export function getStatusBadge(signal) {
  const status = getSignalStatus(signal);
  return `<span class="badge ${status.class}">${status.text}</span>`;
}

export function renderHistoryCard(signal) {
  return `
  <div class="history-card animate-in">
    <div class="card-row header-row">
      <span><strong>${signal.asset || "EUR/USD"}</strong> | ${signal.timeframe || "M15"}</span>
      ${getStatusBadge(signal)}
    </div>
    <div class="card-row direction-row ${signal.direction.toLowerCase()}">
      ${signal.direction} | Conf: ${signal.confidence || 0}%
    </div>
    <div class="card-row">
      Entry: <b>${parseFloat(signal.entry).toFixed(5)}</b>
    </div>
    <div class="card-row">
      TP: <span class="text-green">${parseFloat(signal.tp).toFixed(5)}</span> | SL: <span class="text-red">${parseFloat(signal.sl).toFixed(5)}</span>
    </div>
    <div class="card-row muted">
      ⏱ ${signal.validity || 90} min | ${new Date(signal.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
    </div>
  </div>`;
}

export function renderStats(data) {
  return "";
}
