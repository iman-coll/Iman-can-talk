# Iman's Ollama Chatbot

A Streamlit chatbot that uses [Ollama](https://ollama.com/) open-source models via LangChain for question answering.

| | Link |
|---|---|
| **GitHub** | [iman-coll/OllamaModel-of-Iman-For-Chatbot](https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot) |
| **Deploy (one-click)** | [Deploy on Streamlit Cloud](https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py) |
| **Main app file** | `app.py` |

**Author:** Iman Faisal · [@iman-coll](https://github.com/iman-coll)

---

## How it works

- **GitHub** stores the code.
- **Streamlit Cloud** hosts the chat UI at [share.streamlit.io](https://share.streamlit.io/).
- **Ollama** runs the AI models. Streamlit Cloud cannot run Ollama inside its container, so you point the app at an Ollama server with the `OLLAMA_BASE_URL` secret.

---

## Deploy to Streamlit Cloud

Full steps: **[STREAMLIT-DEPLOY.md](STREAMLIT-DEPLOY.md)**

1. Open the [one-click deploy link](https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py) and sign in with GitHub (`iman-coll`).
2. Confirm **Main file path:** `app.py` → click **Deploy**.
3. Go to **App settings → Secrets** and add your Ollama URL:

```toml
OLLAMA_BASE_URL = "https://your-public-ollama-url"
```

4. **Save** → **Manage app → Reboot**.

See [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example) for a copy-paste template.

### Free Ollama for Streamlit Cloud

Use a **Cloudflare quick tunnel** to expose Ollama on your PC — no payment required.  
Details: **[DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md)** (appendix).

---

## Run locally

For development on your own machine (no secrets needed):

1. Install [Ollama](https://ollama.com/download) and pull a model:

   ```bash
   ollama pull phi3:mini
   ```

2. Install dependencies and run:

   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

3. Optional: copy `.env.example` to `.env` to override `OLLAMA_BASE_URL` or enable LangSmith tracing.

The sidebar shows **Ollama connected** when the server is reachable at `http://127.0.0.1:11434`.

Pull all chatbot models at once (Windows):

```powershell
.\pull-all-models.ps1
```

---

## Features

- Choose from Ollama models: `phi3:mini`, `gemma:2b`, `moondream`, `tinyllama`
- Adjustable temperature and max tokens
- Optional LangSmith tracing
- Works locally or on Streamlit Cloud with a remote Ollama URL

---

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_BASE_URL` | Yes (cloud) | Public Ollama API URL. Local default: `http://127.0.0.1:11434` |
| `LANGCHAIN_API_KEY` | No | LangSmith API key for optional tracing |

On Streamlit Cloud, set `OLLAMA_BASE_URL` in **App settings → Secrets** (not `.env`).

---

## Project structure

```
app.py                              # Streamlit chatbot (Streamlit Cloud entry point)
requirements.txt                    # Python dependencies
.streamlit/
  ├── config.toml                   # Streamlit theme and cloud settings
  └── secrets.toml.example          # Template for Streamlit Cloud secrets
STREAMLIT-DEPLOY.md                 # Deploy guide (GitHub → Streamlit Cloud)
DEPLOY-STEPS-FREE.md                # Appendix: free Ollama (local + Cloudflare tunnel)
docs/optional-railway/ollama-server/  # Optional paid cloud Ollama (Railway/Render) — not required
pull-all-models.ps1                 # Pull all app models locally (Windows)
iman_olama_models_use_for_reasoning.py  # Legacy alias — use app.py instead
```

---

## Optional: paid cloud Ollama

If you prefer hosting Ollama on Railway or Render instead of a tunnel, see **[docs/optional-railway/README.md](docs/optional-railway/README.md)**. This is **not required** for the Streamlit app.
