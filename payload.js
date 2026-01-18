import { renderHistoryRow } from "./signals.js";

const API_BASE = "https://signalgeniusai-production.up.railway.app";
const LATEST_API = `${API_BASE}/signal/latest`;
let refreshInterval = 60;
let countdown = refreshInterval;

async function loadSignal() {
    try {
        const res = await fetch(LATEST_API);
        if (!res.ok) throw new Error("API error");

        const data = await res.json();
        updateFeaturedCard(data);
        addToHistory(data);

        // UI state
        document.getElementById("loading").classList.add("hidden");
        document.getElementById("signal-card").classList.remove("hidden");
    } catch (err) {
        console.error("Fetch failed:", err);
        showError();
    }
}

function updateFeaturedCard(data) {
    // Direct ID updates
    document.getElementById("asset").innerText = data.asset || "EUR/USD";

    const badge = document.getElementById("badge");
    badge.innerText = "LIVE SNAPSHOT";
    badge.className = "badge live";

    const direction = document.getElementById("direction");
    direction.innerText = data.direction || "SCANNING";
    direction.className = `direction ${data.direction}`;

    document.getElementById("entry").innerText = data.entry || "---";
    document.getElementById("tp").innerText = data.tp || "---";
    document.getElementById("sl").innerText = data.sl || "---";

    // Confidence Bar
    const confBar = document.getElementById("confidence-bar");
    const confidence = data.confidence || 0;
    confBar.style.width = `${confidence}%`;

    // Meta
    document.getElementById("strategy").innerText = `Strategy: ${data.strategy || "AI Core v1"}`;
    document.getElementById("timestamp").innerText = `Updated: ${new Date(data.timestamp || Date.now()).toLocaleTimeString()}`;
}

function addToHistory(data) {
    const tbody = document.getElementById("history-tbody");
    if (!tbody) return;

    const rowHtml = renderHistoryRow(data);

    // Create a temporary container to turn string into DOM element
    const temp = document.createElement('tbody');
    temp.innerHTML = rowHtml;
    const row = temp.firstElementChild;

    // Always keep the latest at top
    tbody.prepend(row);

    // Limit history to 10 entries
    if (tbody.children.length > 10) {
        tbody.removeChild(tbody.lastChild);
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
        const timerEl = document.getElementById("refresh-timer");
        if (timerEl) {
            timerEl.innerText = `Refreshing in ${countdown}s`;
        }
    }, 1000);
}

// Initial Run
document.addEventListener("DOMContentLoaded", () => {
    loadSignal();
    startTimer();
});
