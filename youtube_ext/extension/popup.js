const API_URL = "http://localhost:8000/ask";

async function getVideoId() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url) return null;
  const url = new URL(tab.url);
  if (url.hostname.includes("youtube.com")) return url.searchParams.get("v");
  if (url.hostname === "youtu.be") return url.pathname.slice(1);
  return null;
}

document.getElementById("askBtn").addEventListener("click", async () => {
  const answerEl = document.getElementById("answer");
  const question = document.getElementById("question").value.trim();
  if (!question) return;

  const videoId = await getVideoId();
  if (!videoId) {
    answerEl.textContent = "Open a YouTube video first.";
    return;
  }

  answerEl.textContent = "Thinking... (first question on a video takes longer)";
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId, question }),
    });
    const data = await res.json();
    answerEl.textContent = res.ok ? data.answer : `Error: ${data.detail}`;
  } catch (err) {
    answerEl.textContent = "Can't reach the backend. Is uvicorn running?";
  }
});