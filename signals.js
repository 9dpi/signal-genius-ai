export function renderHistoryRow(s) {
  const ageMin = (Date.now() - new Date(s.timestamp)) / 60000;
  const status = ageMin < 60 ? "LIVE" : "EXPIRED";

  return `
    <tr class="animate-in">
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color);">${new Date(s.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color);"><b>${s.asset || "EUR/USD"}</b></td>
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color); color: ${s.direction === 'BUY' ? 'var(--accent-green)' : 'var(--accent-red)'}">
        ${s.direction}
      </td>
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color);">${s.entry}</td>
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color);">${s.tp}</td>
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color);">${s.sl}</td>
      <td style="padding: 12px 8px; border-bottom: 1px solid var(--border-color);">
        <span class="badge ${status.toLowerCase()}">${status}</span>
      </td>
    </tr>
  `;
}

// Keep renderStats for compatibility with payload.js if needed
export function renderStats(data) {
  return "";
}
