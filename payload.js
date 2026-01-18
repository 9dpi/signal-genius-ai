import { renderRow, renderStats } from "./signals.js";

const API_BASE = "https://signalgeniusai-production.up.railway.app";
const LATEST_API = `${API_BASE}/signal/latest`;

async function loadSignal() {
    try {
        const res = await fetch(LATEST_API);
        if (!res.ok) throw new Error("API error");

        const data = await res.json();
        updateUI(data);
    } catch (err) {
        console.error("Fetch failed:", err);
        showError();
    }
}

function updateUI(data) {
    const tbody = document.getElementById("signals-tbody");
    const stats = document.getElementById("stats-container");
    const loading = document.getElementById("loading");

    if (!tbody || !stats) return;

    loading.style.display = "none";

    tbody.innerHTML = renderRow(data);
    stats.innerHTML = renderStats(data);
}

function showError() {
    const loading = document.getElementById("loading");
    if (loading) {
        loading.innerText = "Γ¥î Failed to load signal";
    }
}

document.addEventListener("DOMContentLoaded", loadSignal);
