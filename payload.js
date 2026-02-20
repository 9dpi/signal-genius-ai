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
    // Safe Date Parsing
    const timestamp = data.timestamp;
    const dateObj = (timestamp && !isNaN(new Date(timestamp))) ? new Date(timestamp) : null;

    if (dateObj) {
        // Format: 2026-01-29 14:05:00 UTC (User preference for clarity)
        const dateOptions = { year: 'numeric', month: '2-digit', day: '2-digit' };
        const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false, timeZone: 'UTC' };
        const dStr = dateObj.toLocaleDateString('en-CA', dateOptions); // en-CA gives YYYY-MM-DD
        const tStr = dateObj.toLocaleTimeString('en-GB', timeOptions);
        document.getElementById("card-generated-at").innerText = `${dStr} ${tStr} UTC`;
    } else {
        document.getElementById("card-generated-at").innerText = "— (Historical Record)";
    }

    const statusInfo = getSignalStatus(data);
    const statusEl = document.getElementById("card-status-detailed");

    if (statusEl) {
        if (statusInfo.isLive) {
            statusEl.innerText = "ACTIVE — Monitoring Market";
            statusEl.style.color = "var(--accent-green)";
        } else {
            statusEl.innerText = "EXPIRED (Entry not hit before expiry)";
            statusEl.style.color = "var(--text-secondary)";
        }
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
    document.getElementById("card-volatility").innerText = data.volatility || "Verified";
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

// Tab Switching Logic
function initTabs() {
    const btns = document.querySelectorAll('.tab-btn');
    const panes = document.querySelectorAll('.tab-pane');

    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-tab');

            btns.forEach(b => b.classList.remove('active'));
            panes.forEach(p => p.classList.remove('active'));

            btn.classList.add('active');
            const targetPane = document.getElementById(target);
            if (targetPane) {
                targetPane.classList.add('active');
            }

            if (target === 'tab-logs') {
                fetchLogs();
            }
        });
    });
}

const AI_CORE_API = 'https://quantixaicore-production.up.railway.app/api/v1';

async function fetchLogs() {
    const tbody = document.getElementById('logs-body');
    if (!tbody) return;

    // Also refresh heartbeat
    fetchHeartbeat();

    try {
        tbody.innerHTML = '<tr><td colspan="6" class="empty-state">Loading validation data...</td></tr>';
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 8000);

        let res = await fetch(`${AI_CORE_API}/validation-logs?limit=50`, { signal: controller.signal });
        clearTimeout(timeoutId);

        const json = await res.json();
        if (json.success && json.data) {
            tbody.innerHTML = '';
            if (json.data.length === 0) {
                tbody.innerHTML = '<tr><td colspan="6" class="empty-state">No validation events recorded yet (Waiting for first signal).</td></tr>';
                return;
            }
            json.data.forEach(log => {
                const tr = document.createElement('tr');
                const isDisc = log.is_discrepancy;
                const statusColor = isDisc ? '#ef4444' : '#10b981';
                const statusIcon = isDisc ? '⚠️' : '✅';
                const statusText = isDisc ? 'MISMATCH' : 'MATCHED';

                let ts = new Date(log.created_at).toLocaleString();

                // Proof (Candle Data)
                let proof = '';
                if (log.validator_candle) {
                    const c = log.validator_candle;
                    proof = `O:${c.open} H:${c.high} L:${c.low} C:${c.close}`;
                } else {
                    proof = 'No Candle Data';
                }

                let meta = log.meta_data ? (typeof log.meta_data === 'string' ? log.meta_data : JSON.stringify(log.meta_data)) : '';

                tr.innerHTML = `
                    <td class="mono" style="color:#64748b; font-size:0.7rem">${ts}</td>
                    <td class="mono" style="color:var(--primary-cyan)">${log.signal_id ? log.signal_id.slice(0, 4) : '--'}</td>
                    <td style="font-weight:600; font-size:0.75rem">${log.check_type || 'UNKNOWN'}</td>
                    <td class="mono">${Number(log.validator_price || 0).toFixed(5)}</td>
                    <td style="color:${statusColor}; font-weight:800; font-size:0.75rem;">${statusIcon} ${statusText}</td>
                    <td style="color:#64748b; font-size:0.7rem;">
                        <div style="font-weight:700; color:#475569">Proof: ${proof}</div>
                        <div style="margin-top:2px; font-style:italic">${meta}</div>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }
    } catch (e) {
        tbody.innerHTML = `<tr><td colspan="6" class="empty-state" style="color:#ef4444">⚠️ Connection to AI Core failed. Retrying...</td></tr>`;
    }
}

async function fetchHeartbeat() {
    const hbody = document.getElementById('heartbeat-body');
    if (!hbody) return;

    try {
        const res = await fetch(`${AI_CORE_API}/analysis-logs?limit=20`);
        const json = await res.json();

        if (json.success && json.data) {
            hbody.innerHTML = '';
            json.data.forEach(beat => {
                const tr = document.createElement('tr');
                const ts = new Date(beat.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
                const conf = Math.round((beat.release_confidence || beat.confidence) * 100);
                const strength = Math.round(beat.strength * 100);
                const color = conf >= 65 ? 'var(--accent-green)' : '#64748b';

                tr.innerHTML = `
                    <td class="mono" style="color:#64748b; font-size:0.7rem">${ts}</td>
                    <td style="font-weight:700">${beat.asset}</td>
                    <td style="color:${color}; font-weight:800; font-size:0.75rem">${beat.status}</td>
                    <td class="mono" style="font-weight:700; color:${color}">${conf}%</td>
                    <td class="mono" style="color:#94a3b8">${strength}%</td>
                    <td style="color:#64748b; font-size:0.7rem; font-style:italic">${beat.refinement || 'Standard scan'}</td>
                `;
                hbody.appendChild(tr);
            });
        }
    } catch (e) {
        console.warn("Heartbeat fetch failed");
    }
}

// Global Exports
window.fetchLogs = fetchLogs;

// Initial Run
document.addEventListener("DOMContentLoaded", () => {
    loadSignal();
    startTimer();
    initTabs();
});
