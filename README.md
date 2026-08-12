# Iman's Ollama Chatbot

A Streamlit chatbot that uses [Ollama](https://ollama.com/) open-source models via LangChain for question answering.

## Features

- Choose from multiple Ollama models (phi3:mini, gemma:2b, moondream, tinyllama)
- Adjustable temperature and max tokens
- Optional LangSmith tracing for debugging
- Works locally **or** on [Streamlit Community Cloud](https://share.streamlit.io/) with a remote Ollama server

---

## Deploy to Streamlit Cloud (recommended path)

Streamlit Cloud **cannot** run Ollama inside its container. Deploy Ollama separately, then connect the app.

### Step 1 — Deploy Ollama to Railway (~5 min)

Follow the guide: **[deploy/ollama-server/README.md](deploy/ollama-server/README.md)**

Quick summary:

1. Sign up at [railway.app](https://railway.app/)
2. **New Project → Deploy from GitHub** → select this repo
3. Set **Root Directory** to `deploy/ollama-server`
4. **Settings → Networking → Generate Domain** → copy the URL
5. Wait for deploy logs to show `Model pull complete` (first run: 10–30 min)

Test: open `https://YOUR-URL.up.railway.app/api/tags` in a browser.

### Step 2 — Deploy this Streamlit app

1. Go to [share.streamlit.io](https://share.streamlit.io/) → sign in with GitHub
2. **New app** → select **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**
3. **Main file path:** `app.py`
4. **App settings → Secrets** — paste:

```toml
OLLAMA_BASE_URL = "https://YOUR-URL.up.railway.app"
```

5. Click **Deploy** (or **Reboot** if already deployed)

The sidebar should show **Ollama connected**. Start chatting!

> See also [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) for a copy-paste template.

### Alternative: Render

Render free tier works but has cold starts. See [deploy/ollama-server/README.md](deploy/ollama-server/README.md#option-b-render-free-tier-slower-cold-starts).

### Free public Ollama API?

There is **no reliable free public Ollama endpoint** suitable for production demos. Community tunnels (ngrok, etc.) are temporary. **Self-hosted Railway Ollama** (Step 1 above) is the intended path and stays under free-tier credits for light use.

---

## Local Setup

For development on your own machine:

1. Install [Ollama](https://ollama.com/download):
   - **Windows:** Download and run the installer. Ollama starts in the system tray.
   - **macOS / Linux:** Install from ollama.com, then `ollama serve` if needed.

2. Verify Ollama is running:

   ```bash
   ollama --version
   curl http://127.0.0.1:11434/api/tags
   ```

3. Pull a model:

   ```bash
   ollama pull phi3:mini
   ```

4. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Copy `.env.example` to `.env`:

   ```
   OLLAMA_BASE_URL=http://127.0.0.1:11434
   LANGCHAIN_API_KEY=your_langsmith_api_key
   ```

   Use `127.0.0.1` instead of `localhost` to avoid IPv6 connection errors.

6. Run the app:

   ```bash
   streamlit run app.py
   ```

The sidebar shows **Ollama connected** when the server is reachable.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_BASE_URL` | Yes (cloud) | Ollama API URL. Local default: `http://127.0.0.1:11434`. Cloud: your Railway URL. |
| `LANGCHAIN_API_KEY` | No | LangSmith API key for optional tracing |

On Streamlit Cloud, `OLLAMA_BASE_URL` **must** be set in **App settings → Secrets** (not `.env`).

---

## Project structure

```
app.py                          # Streamlit chatbot
deploy/ollama-server/           # Docker + Railway/Render deploy for remote Ollama
  ├── Dockerfile
  ├── start.sh                  # Pulls phi3:mini, gemma:2b, moondream, tinyllama
  ├── railway.toml
  ├── render.yaml
  └── README.md                 # Step-by-step Railway deploy
.streamlit/secrets.toml.example # Template for Streamlit Cloud secrets
```

---

## Author

**Iman Faisal** ([@iman-coll](https://github.com/iman-coll))
