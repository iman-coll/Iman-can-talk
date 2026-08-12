# Optional: Paid Cloud Ollama

> **Not required.** The main app deploys on [Streamlit Cloud](https://share.streamlit.io/) from GitHub. For a **free** Ollama URL, use the [Cloudflare tunnel appendix](../DEPLOY-STEPS-FREE.md) instead.

This folder contains Docker configs to run Ollama on **Railway** or **Render** — useful if you have credits and want 24/7 cloud Ollama without keeping your PC on.

**Author:** Iman Faisal · [@iman-coll](https://github.com/iman-coll)

---

## When to use this

| Use this | Use free appendix instead |
|----------|----------------------------|
| You have Railway/Render credits | You want $0 hosting |
| PC should stay off | PC can stay on with a tunnel |
| Stable public URL without tunnel | Quick demo with Cloudflare |

---

## Deploy on Railway

1. Go to [railway.app](https://railway.app/) → **New Project** → **Deploy from GitHub repo**.
2. Select **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**.
3. **Settings → Root Directory:** `docs/optional-railway/ollama-server`
4. **Settings → Networking → Generate Domain** → copy your URL.
5. Wait for deploy logs: `Model pull complete. Ollama server is running.`
6. Test: `https://YOUR-URL.up.railway.app/api/tags`
7. Set Streamlit secret:

```toml
OLLAMA_BASE_URL = "https://YOUR-URL.up.railway.app"
```

See [ollama-server/README.md](ollama-server/README.md) for Render, memory notes, and troubleshooting.

---

## Files

| Path | Purpose |
|------|---------|
| `ollama-server/Dockerfile` | Ollama Docker image |
| `ollama-server/start.sh` | Starts server and pulls models |
| `ollama-server/railway.toml` | Railway config |
| `ollama-server/render.yaml` | Render Blueprint |
| `ollama-server/README.md` | Detailed Railway/Render steps |
