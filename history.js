/**
 * History Page Logic
 * Fetches and renders the immutable signal ledger
 */

const API_HISTORY_URL = "https://signalgeniusai-production.up.railway.app/api/v1/signals/history";

async function loadHistory() {
  const historyBody = document.getElementById("history-body");
  const statsSummary = document.getElementById("stats-summary");

  try {
    const response = await fetch(API_HISTORY_URL);
    const data = await response.json();

    if (data.status !== "ok") throw new Error("API failed");

    // 1. Render Stats
    const stats = data.stats;
    statsSummary.innerHTML = `
      <div class="stat-card">
        <div class="stat-value">${stats.win_rate}%</div>
        <div class="stat-label">Win Rate</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${stats.total}</div>
        <div class="stat-label">Total Signals</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${stats.avg_pips}</div>
        <div class="stat-label">Avg Pips</div>
      </div>
      <div class="stat-card">
        <div class="stat-value">${stats.win}/${stats.loss}</div>
        <div class="stat-label">Win/Loss</div>
      </div>
    `;


    // 2. Render Table
    historyBody.innerHTML = data.signals.map(s => {
      const date = new Date(s.created_at).toLocaleDateString('en-GB', {
        day: '2-digit',
        month: 'short'
      });

      const outcomeClass = {
        "TP_HIT": "outcome-win",
        "SL_HIT": "outcome-loss",
        "EXPIRED": "outcome-exp",
        "OPEN": "outcome-act",
        "CREATED": "outcome-act"
      }[s.status] || "";

      const outcomeText = {
        "TP_HIT": "🟢 WIN",
        "SL_HIT": "🔴 LOSS",
        "EXPIRED": "⚪ EXPIRED",
        "OPEN": "⏳ OPEN",
        "CREATED": "🕒 CREATED"
      }[s.status] || s.status;


      return `
        <tr>
          <td>${date}</td>
          <td class="history-symbol">${s.symbol}</td>
          <td class="history-direction ${s.direction.toLowerCase()}">${s.direction}</td>
          <td>${s.entry[0]}</td>
          <td>${s.tp}</td>
          <td>${s.sl}</td>
          <td class="${outcomeClass}">${outcomeText}</td>
          <td>${s.confidence}%</td>
        </tr>
      `;
    }).join("");

  } catch (err) {
    console.error("History load error:", err);
    if (historyBody) {
      historyBody.innerHTML = `<tr><td colspan="8" style="text-align:center; padding: 40px; color: #ef4444;">⚠️ Failed to load history. Please try again later.</td></tr>`;
    }
  }
}

// Initial load
loadHistory();
