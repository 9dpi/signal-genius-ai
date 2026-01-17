/**
 * Payload - Data Fetching and Orchestration
 * (Production Bento UI Version)
 */

import { renderRow, renderStats } from "./signals.js";

const API_BASE = "https://signalgeniusai-production.up.railway.app";
const LATEST_API = `${API_BASE}/api/v1/signals/history`;

function updateUI(data) {
    const root = document.getElementById("signals-tbody");
    const statsRoot = document.getElementById("stats-container");
    if (!root || !statsRoot) return;

    if (!data || data.status !== "ok") {
        root.innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 40px; color: var(--text-muted);">API Unreachable</td></tr>';
        return;
    }

    // 1. Update stats summary
    statsRoot.innerHTML = renderStats(data.stats);

    // 2. Update signals table (last 7)
    const signals = data.signals || [];
    root.innerHTML = signals.slice(0, 7).map(s => renderRow(s)).join("");
}

async function fetchAndRefresh() {
    try {
        const response = await fetch(LATEST_API);
        if (!response.ok) throw new Error("Network error");
        const data = await response.json();
        updateUI(data);
    } catch (err) {
        console.error("Fetch error:", err);
        updateUI(null);
    }
}

// Initial load
fetchAndRefresh();

// Auto-refresh every 15 seconds for live tracking feel
setInterval(fetchAndRefresh, 15000);
