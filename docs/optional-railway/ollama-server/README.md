# Deploy Ollama Server to the Cloud (Optional)

> **Not required for the Streamlit app.** For free hosting, use **[DEPLOY-STEPS-FREE.md](../../DEPLOY-STEPS-FREE.md)** (Cloudflare tunnel) or run locally.  
> **Main deploy guide:** [STREAMLIT-DEPLOY.md](../../STREAMLIT-DEPLOY.md)

This folder runs a **remote Ollama API** for users who prefer **paid cloud hosting** (Railway or Render) instead of a tunnel.

**Models pulled on first start:** `phi3:mini` (default). Set env `OLLAMA_EXTRA_MODELS=gemma:2b,moondream,tinyllama` to pull more if your plan has enough RAM.

---

## Option A: Railway

1. Go to [railway.app](https://railway.app/) and sign up (GitHub login).
2. **New Project** → **Deploy from GitHub repo** → select **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**.
3. **Settings → Root Directory:** `docs/optional-railway/ollama-server`
4. **Settings → Networking → Generate Domain** → copy your public URL.
5. Wait for deploy logs: `Model pull complete. Ollama server is running.`
6. Test: `curl https://YOUR-RAILWAY-URL.up.railway.app/api/tags`
7. In Streamlit → **App settings → Secrets**:

```toml
OLLAMA_BASE_URL = "https://YOUR-RAILWAY-URL.up.railway.app"
```

Save and **Reboot app**.

---

## Option B: Render

Render’s free tier has **512 MB RAM** — often too small for `phi3:mini` (~2.3 GB). Use a paid instance or pull only one model.

1. Go to [render.com](https://render.com/) → **New → Blueprint** (or **New Web Service**).
2. Connect repo `iman-coll/OllamaModel-of-Iman-For-Chatbot`.
3. Set **Root Directory** to `docs/optional-railway/ollama-server`.
4. Deploy and copy the `*.onrender.com` URL.
5. Use that URL as `OLLAMA_BASE_URL` in Streamlit secrets.

---

## Memory notes

| Model | Approx. size |
|-------|--------------|
| tinyllama | ~0.6 GB |
| gemma:2b | ~1.6 GB |
| phi3:mini | ~2.3 GB |
| moondream | ~1.7 GB |

Default deploy pulls only `phi3:mini`. Add `OLLAMA_EXTRA_MODELS=gemma:2b,moondream,tinyllama` on plans with **6+ GB RAM**.

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| Streamlit shows setup message | Add `OLLAMA_BASE_URL` in Streamlit secrets and reboot |
| `502` / timeout on Railway | Wait for model pulls to finish in deploy logs |
| Model not found in chat | Check `/api/tags` — re-run deploy |
| Render OOM | Free 512 MB too small — use Cloudflare tunnel or upgrade plan |

---

## Security

This setup exposes Ollama **without authentication**. Fine for demos; add auth or VPN for production.

---

## Files

| File | Purpose |
|------|---------|
| `Dockerfile` | Official `ollama/ollama` image + startup script |
| `start.sh` | Starts server, pulls models |
| `railway.toml` | Railway health check & Docker build |
| `render.yaml` | Render Blueprint config |
