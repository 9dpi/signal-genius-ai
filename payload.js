/**
 * Payload – Data Fetching and Orchestration
 * Production Bento UI Version
 */

import { renderRow, renderStats } from "./signals.js";

const API_BASE = "https://signalgeniusai-production.up.railway.app";
const LATEST_API = `${API_BASE}/signal/latest`;

function updateUI(data) {
    // Bento UI structure usually has 'signal-container' or similar, 
    // but if the user insists on 'signals-tbody' logic from Bento Grid Table version:
    // Wait, user's provided logic references 'signals-tbody'.
    // Let's stick EXACTLY to user's provided code for payload.js

    const root = document.getElementById("signals-tbody");
    const statsRoot = document.getElementById("stats-container");

    if (!root || !statsRoot || !data) return;

    // Adapt to the data structure - if data IS the signal (flat), wrap it?
    // Or if renderRow handles the object directly.
    root.innerHTML = renderRow(data);
    statsRoot.innerHTML = renderStats(data);
}

async function fetchLatestSignal() {
    try {
        const res = await fetch(LATEST_API);
        const data = await res.json();
        updateUI(data);
    } catch (err) {
        console.error("Fetch error:", err);
    }
}

// Initial load
fetchLatestSignal();

// Auto refresh (live tracker feel)
setInterval(fetchLatestSignal, 15000);
