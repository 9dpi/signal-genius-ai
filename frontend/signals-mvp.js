/**
 * Signal Genius AI - MVP Frontend
 * Connects to Railway backend and displays signal data
 */

const API_URL = "https://signalgeniusai-production.up.railway.app/api/v1/signal/latest";

document.addEventListener("DOMContentLoaded", async () => {
  const el = document.getElementById("signal");
  
  if (!el) {
    console.error("Element with id 'signal' not found!");
    return;
  }
  
  el.innerText = "Loading signal data...";

  try {
    const res = await fetch(API_URL);
    
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`);
    }
    
    const data = await res.json();
    
    // Display raw JSON for MVP
    el.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    
    console.log("✅ Signal data loaded:", data);
    
  } catch (e) {
    el.innerHTML = `
      <div style="color: red; padding: 20px; border: 2px solid red; border-radius: 8px;">
        <h3>⚠️ API Error</h3>
        <p>${e.message}</p>
        <p><small>Check console for details</small></p>
      </div>
    `;
    console.error("❌ Error fetching signal:", e);
  }
});
