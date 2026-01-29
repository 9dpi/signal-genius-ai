import { renderHistoryCard, getSignalStatus } from "./signals.js";

const API_BASE = "https://signalgeniusai-production.up.railway.app";
const LATEST_API = `${API_BASE}/signal/latest`;
let refreshInterval = 60;
let countdown = refreshInterval;

let lastSignalTimestamp = null;

async function loadSignal() {
    try {
        const res = await fetch(LATEST_API);
        if (!res.ok) throw new Error("API error");

        const data = await res.json();

        // GLOBAL STATUS CHECK: MARKET CLOSED
        if (data.status === "MARKET_CLOSED") {
            document.getElementById("loading").classList.add("hidden");
            document.getElementById("signal-card").classList.add("hidden");
            document.getElementById("market-closed").classList.remove("hidden");
            return; // Stop processing
        } else {
            document.getElementById("market-closed").classList.add("hidden");
        }

        updateFeaturedCard(data);

        // Only add to history if it's a new signal
        if (data.timestamp !== lastSignalTimestamp) {
            addToHistory(data);
            lastSignalTimestamp = data.timestamp;
        }

        // UI state
        document.getElementById("loading").classList.add("hidden");
        document.getElementById("signal-card").classList.remove("hidden");
    } catch (err) {
        console.error("Fetch failed:", err);
        showError();
    }
}

function updateFeaturedCard(data) {
    // Top Section
    const now = new Date(data.timestamp || Date.now());

    // Format: 21 Jan 2026 · 06:09 UTC
    const dateOptions = { day: 'numeric', month: 'short', year: 'numeric' };
    const timeOptions = { hour: '2-digit', minute: '2-digit', timeZone: 'UTC' };
    const dateStr = now.toLocaleDateString('en-GB', dateOptions);
    const timeStr = now.toLocaleTimeString('en-GB', timeOptions);

    document.getElementById("card-generated-at").innerText = `${dateStr} · ${timeStr} UTC`;

    const statusInfo = getSignalStatus(data);
    const statusEl = document.getElementById("card-main-status");

    if (statusInfo.isLive) {
        statusEl.innerText = "Active — Monitoring Market";
        statusEl.className = "meta-value status-text live";
    } else {
        statusEl.innerText = "EXPIRED — no longer active";
        statusEl.className = "meta-value status-text expired";
    }

    // Main Info
    document.getElementById("card-asset").innerText = `📊 ${data.asset || "EUR/USD"}`;
    document.getElementById("card-tf").innerText = data.timeframe || "M15";

    const dirText = document.getElementById("dir-text");
    const direction = data.direction ? data.direction.toUpperCase() : "WAIT";

    if (direction === 'BUY') {
        dirText.innerText = "🟢 BUY";
        dirText.className = "BUY";
    } else if (direction === 'SELL') {
        dirText.innerText = "🔴 SELL";
        dirText.className = "SELL";
    } else {
        dirText.innerText = `⚪ ${direction}`;
        dirText.className = "NEUTRAL";
    }

    document.getElementById("strength-text").innerText = data.strength || "(MID)";

    // Levels
    const formatPrice = (val) => val ? parseFloat(val).toFixed(5) : "---";
    document.getElementById("card-entry").innerText = formatPrice(data.entry);
    document.getElementById("card-tp").innerText = formatPrice(data.tp);
    document.getElementById("card-sl").innerText = formatPrice(data.sl);

    // Analysis
    document.getElementById("card-confidence").innerText = `${data.confidence || 0}%`;
    document.getElementById("card-strategy").innerText = data.strategy || "Trend Follow";

    // UI - Use real data from API
    document.getElementById("card-validity").innerText = `${data.validity_passed || 81} / ${data.validity || 90} min`;
    document.getElementById("card-volatility").innerText = data.volatility || "0.12% (Stabilized)";
}

function addToHistory(data) {
    const container = document.getElementById("history-container");
    if (!container) return;

    const cardHtml = renderHistoryCard(data);

    // Create a temporary container to turn string into DOM element
    const temp = document.createElement('div');
    temp.innerHTML = cardHtml;
    const card = temp.firstElementChild;

    // Always keep the latest at top
    container.prepend(card);

    // Limit history to 10 entries
    if (container.children.length > 10) {
        container.removeChild(container.lastChild);
    }
}

function showError() {
    const loading = document.getElementById("loading");
    if (loading) {
        loading.innerHTML = `<h2 style="color: var(--accent-red)">⚠️ Connection Error</h2><p>Unable to reach AI Signal Engine.</p>`;
    }
}

function startTimer() {
    setInterval(() => {
        countdown--;
        if (countdown <= 0) {
            countdown = refreshInterval;
            loadSignal();
        }
        const timerEl = document.getElementById("refresh-indicator");
        if (timerEl) {
            timerEl.innerText = `Auto-refresh active in ${countdown}s`;
        }
    }, 1000);
}

// Initial Run
document.addEventListener("DOMContentLoaded", () => {
    loadSignal();
    startTimer();
});
