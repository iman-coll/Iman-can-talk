# Deploy on Streamlit Cloud

**Repo:** [iman-coll/OllamaModel-of-Iman-For-Chatbot](https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot)  
**Author:** Iman Faisal · [@iman-coll](https://github.com/iman-coll)

GitHub stores the code. Streamlit Cloud runs the app. You still need a reachable **Ollama server** for chat to work.

---

## One-click deploy

1. Open:  
   **https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py**
2. Sign in with **GitHub** (`iman-coll`).
3. Confirm settings:
   - **Repository:** `iman-coll/OllamaModel-of-Iman-For-Chatbot`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **Deploy**.

Streamlit reads `requirements.txt` and `.streamlit/config.toml` automatically.

---

## Required secret: `OLLAMA_BASE_URL`

Streamlit Cloud **cannot** reach `localhost` or `127.0.0.1` on your PC. After the first deploy:

1. Open your app on [share.streamlit.io](https://share.streamlit.io/).
2. Go to **App settings → Secrets**.
3. Paste (replace with your public Ollama URL):

```toml
OLLAMA_BASE_URL = "https://your-public-ollama-url"
```

4. Click **Save** → **Manage app → Reboot app**.

Test your Ollama URL in a browser: `https://your-public-ollama-url/api/tags` — you should see JSON listing models.

Template: [.streamlit/secrets.toml.example](.streamlit/secrets.toml.example)

---

## Where to get a public Ollama URL

| Path | Cost | Guide |
|------|------|-------|
| **Local Ollama + Cloudflare tunnel** | Free | [DEPLOY-STEPS-FREE.md § Cloudflare](DEPLOY-STEPS-FREE.md#cloudflare-quick-tunnel-for-streamlit-cloud) |
| **Run locally only (no cloud)** | Free | [DEPLOY-STEPS-FREE.md § Local](DEPLOY-STEPS-FREE.md#run-locally-no-streamlit-cloud) |
| **Paid cloud Ollama (Railway/Render)** | Paid | [docs/optional-railway/README.md](docs/optional-railway/README.md) |

**Recommended free path for Streamlit Cloud:** Cloudflare quick tunnel — see the appendix.

---

## Verify

1. Sidebar shows **Ollama connected**.
2. Pick a model (e.g. `phi3:mini`) and send a test message.

If the app shows a setup message instead, add or fix `OLLAMA_BASE_URL` in secrets and reboot.

---

## Quick links

| What | URL |
|------|-----|
| GitHub repo | https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot |
| Streamlit deploy | https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py |
| Free Ollama appendix | [DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md) |
