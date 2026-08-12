# Iman's Ollama Chatbot

A Streamlit chatbot that uses [Ollama](https://ollama.com/) open-source models via LangChain for question answering.

**Easiest deploy guide:** [DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md) — free options (local Ollama + tunnel, Render, etc.) for [@iman-coll](https://github.com/iman-coll).

**Railway guide (if you have credits):** [DEPLOY-STEPS.md](DEPLOY-STEPS.md)

## Features

- Choose from multiple Ollama models (phi3:mini, gemma:2b, moondream, tinyllama)
- Adjustable temperature and max tokens
- Optional LangSmith tracing for debugging
- Works locally **or** on [Streamlit Community Cloud](https://share.streamlit.io/) with a remote Ollama server

---

## Deploy to Streamlit Cloud (recommended path)

Streamlit Cloud **cannot** run Ollama inside its container. Deploy Ollama separately (or expose local Ollama), then connect the app.

**Start here if Railway trial expired:** **[DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md)** — **local Streamlit** ($0, 2 min) or **Cloudflare tunnel** for Streamlit Cloud. No ngrok payment needed.

### Step 1 — Expose Ollama (pick one)

| Path | Guide |
|------|--------|
| **Free — run locally (easiest, no tunnel)** | [DEPLOY-STEPS-FREE.md § Option 1](DEPLOY-STEPS-FREE.md#option-1--local-streamlit-simplest-100-free) |
| **Free — Streamlit Cloud + Cloudflare tunnel** | [DEPLOY-STEPS-FREE.md § Option 2](DEPLOY-STEPS-FREE.md#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud) |
| Railway (needs credits) | [deploy/ollama-server/README.md](deploy/ollama-server/README.md) |
| Render (512 MB free tier often too small) | [DEPLOY-STEPS-FREE.md § Option A](DEPLOY-STEPS-FREE.md#option-a--render-existing-renderyaml) |

Copy your public Ollama URL (e.g. `https://something.trycloudflare.com`). Test: `https://YOUR-URL/api/tags`.

### Step 2 — Deploy this Streamlit app

1. Go to [share.streamlit.io](https://share.streamlit.io/) → sign in with GitHub
2. **New app** → select **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**
3. **Main file path:** `app.py`
4. **App settings → Secrets** — paste:

```toml
OLLAMA_BASE_URL = "https://YOUR-PUBLIC-OLLAMA-URL"
```

5. Click **Deploy** (or **Reboot** if already deployed)

The sidebar should show **Ollama connected**. Start chatting!

> See also [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) for a copy-paste template.

### Free hosting after Railway expires

There is **no reliable free public Ollama API** run by a third party. Practical $0 paths:

- **Local Streamlit** — run on your PC, zero setup ([DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md))
- **Local Ollama + Cloudflare Tunnel** — for share.streamlit.io ([DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md))
- **Render** — `render.yaml` included; free tier has cold starts and **512 MB RAM** (often too small for models)
- **Oracle Cloud Always Free VM** — full cloud Ollama, more setup

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
   py -3 -m streamlit run app.py
   ```

The sidebar shows **Ollama connected** when the server is reachable.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_BASE_URL` | Yes (cloud) | Ollama API URL. Local default: `http://127.0.0.1:11434`. Cloud: tunnel or cloud deploy URL. |
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
