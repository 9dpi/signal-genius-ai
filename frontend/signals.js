<<<<<<< HEAD
function renderTelegramMessage(data) {
  if (!data || data.status !== "ok" || !data.payload) {
    return "⚠️ No valid signal data available.";
  }

  const p = data.payload;

  const directionEmoji = p.direction === "BUY" ? "🟢 BUY" : "🔴 SELL";
  const confidenceEmoji =
    p.confidence >= 95 ? "🔥" :
      p.confidence >= 90 ? "⚡" :
        "⚠️";

  return `
${directionEmoji} ${p.asset} (${p.timeframe})

ENTRY: ${p.entry[0].toFixed(5)} – ${p.entry[1].toFixed(5)}
TP: ${p.tp.toFixed(5)}
SL: ${p.sl.toFixed(5)}

CONFIDENCE: ${p.confidence}% ${confidenceEmoji}
SESSION: ${p.session}
`.trim();
}
=======
function renderTelegramMessage(data) {
  if (!data || data.status !== "ok" || !data.payload) {
    return "⚠️ No valid signal data available.";
  }

  const p = data.payload;

  const directionEmoji = p.direction === "BUY" ? "🟢 BUY" : "🔴 SELL";
  const confidenceEmoji =
    p.confidence >= 95 ? "🔥" :
      p.confidence >= 90 ? "⚡" :
        "⚠️";

  return `
${directionEmoji} ${p.asset} (${p.timeframe})

ENTRY: ${p.entry[0].toFixed(5)} – ${p.entry[1].toFixed(5)}
TP: ${p.tp.toFixed(5)}
SL: ${p.sl.toFixed(5)}

CONFIDENCE: ${p.confidence}% ${confidenceEmoji}
SESSION: ${p.session}
`.trim();
}
>>>>>>> de67d7e0b5c7e2b6c648edaac0ac82a61fb55248
