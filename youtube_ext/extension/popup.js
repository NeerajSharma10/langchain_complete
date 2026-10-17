const API_URL = "http://127.0.0.1:8000";

const $ = (id) => document.getElementById(id);
const videoEl = $("video");
const questionEl = $("question");
const askBtn = $("ask");
const resultEl = $("result");

let videoId = null;

function getVideoId(url) {
  try {
    const u = new URL(url);
    if (u.hostname === "youtu.be") return u.pathname.slice(1) || null;
    if (u.hostname.endsWith("youtube.com")) {
      if (u.pathname === "/watch") return u.searchParams.get("v");
      const m = u.pathname.match(/^\/(shorts|embed|live)\/([\w-]{11})/);
      if (m) return m[2];
    }
  } catch (_) {}
  return null;
}

function show(text, kind = "") {
  resultEl.hidden = false;
  resultEl.className = kind;
  resultEl.textContent = text;
}

async function init() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  videoId = tab && tab.url ? getVideoId(tab.url) : null;

  if (!videoId) {
    videoEl.textContent = "Open a YouTube video to ask about it.";
    return;
  }

  videoEl.textContent = (tab.title || "").replace(/ - YouTube$/, "") || videoId;
  questionEl.disabled = false;
  askBtn.disabled = false;
  questionEl.focus();
}

async function ask() {
  const question = questionEl.value.trim();
  if (!videoId || !question) return;

  askBtn.disabled = true;
  questionEl.disabled = true;
  show("Reading the transcript. The first question on a video takes a bit longer.", "status");

  try {
    const res = await fetch(`${API_URL}/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ video_id: videoId, question }),
    });
    const data = await res.json().catch(() => ({}));

    if (!res.ok) {
      show(data.detail || `Request failed (${res.status}).`, "error");
    } else {
      show(data.answer || "No answer came back.");
    }
  } catch (_) {
    show(
      "Can't reach the backend. Start it with: python3 youtube_ext/backend/main.py",
      "error"
    );
  } finally {
    askBtn.disabled = false;
    questionEl.disabled = false;
    questionEl.focus();
  }
}

askBtn.addEventListener("click", ask);
questionEl.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    ask();
  }
});

init();