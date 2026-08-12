# Deploy Ollama Server to the Cloud

> **Railway trial expired?** Use **[DEPLOY-STEPS-FREE.md](../../DEPLOY-STEPS-FREE.md)** — easiest path is **local Ollama + ngrok/Cloudflare tunnel** ($0). Render steps below; free tier is 512 MB RAM (often too small for models).

This folder runs a **remote Ollama API** so your [Streamlit chatbot](https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot) on **Streamlit Community Cloud** can reach it.

Streamlit Cloud **cannot** run `ollama serve` inside its container (no GPU, limited RAM, no persistent daemon). You deploy Ollama here instead, then point the Streamlit app at your public URL.

**Models pulled on first start:** `phi3:mini` (default). Set env `OLLAMA_EXTRA_MODELS=gemma:2b,moondream,tinyllama` to pull more if your plan has enough RAM.

---

## Option A: Railway (recommended — ~5 minutes)

Railway is the easiest path: connect GitHub, set one folder, deploy.

### 1. Create a Railway account

1. Go to [railway.app](https://railway.app/) and sign up (GitHub login works).
2. You get **$5/month free credit** on the Hobby plan — enough for light demo use.

### 2. Deploy this Ollama service

1. Click **New Project** → **Deploy from GitHub repo**.
2. Select **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**.
3. When the service is created, open **Settings**:
   - **Root Directory:** `deploy/ollama-server`
   - **Watch Paths:** leave default or set to `deploy/ollama-server/**`
4. Open **Settings → Networking** → **Generate Domain**.
5. Copy your public URL, e.g. `https://iman-ollama-production.up.railway.app`  
   (no trailing slash, no `:11434` — Railway proxies to the internal `PORT` for you).

### 3. Wait for models to download

1. Open **Deployments** → latest deploy → **View Logs**.
2. First boot pulls `phi3:mini` by default — usually **5–15 minutes**. Add `OLLAMA_EXTRA_MODELS` in Railway variables to pull more models.
3. When you see `Model pull complete. Ollama server is running.`, the server is ready.

### 4. Test the server

In a browser or terminal:

```bash
curl https://YOUR-RAILWAY-URL.up.railway.app/api/tags
```

You should get JSON listing installed models.

### 5. Connect Streamlit Cloud

In your Streamlit app → **App settings → Secrets**, add:

```toml
OLLAMA_BASE_URL = "https://YOUR-RAILWAY-URL.up.railway.app"
```

Save and **Reboot app**. The chatbot sidebar should show **Ollama connected**.

---

## Option B: Render (free tier, slower cold starts)

Render’s free tier **spins down after inactivity** (~15 min). First request after sleep can take 1–2 minutes.

### Steps

1. Go to [render.com](https://render.com/) and sign up.
2. **New → Blueprint** (or **New Web Service**).
3. Connect repo `iman-coll/OllamaModel-of-Iman-For-Chatbot`.
4. Set **Root Directory** to `deploy/ollama-server`.
5. Render reads `render.yaml` automatically, or set:
   - **Runtime:** Docker
   - **Health check path:** `/api/tags`
6. Deploy and copy the `*.onrender.com` URL.
7. Use that URL as `OLLAMA_BASE_URL` in Streamlit secrets (same as Railway step 5).

---

## Memory & cost notes

| Model        | Approx. size |
|-------------|--------------|
| tinyllama   | ~0.6 GB      |
| gemma:2b    | ~1.6 GB      |
| phi3:mini   | ~2.3 GB      |
| moondream   | ~1.7 GB      |

All four models need **~6+ GB RAM**. Railway/Render free tiers may be tight:

- **Tip:** Default deploy pulls only `phi3:mini`. Add Railway env `OLLAMA_EXTRA_MODELS=gemma:2b,moondream,tinyllama` if you have **6+ GB RAM**.
- If deploy fails with OOM, keep only `phi3:mini` (default) or upgrade the plan.

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| Streamlit shows “Deploy Ollama server first” | Add `OLLAMA_BASE_URL` in Streamlit secrets and reboot |
| `502` / timeout on Railway | Wait for model pulls to finish in deploy logs |
| Model not found in chat | Check `/api/tags` — re-run deploy or `ollama pull <model>` in logs |
| Render very slow first message | Free tier woke from sleep — normal |

---

## Security (production)

This setup exposes Ollama **without authentication**. For a public demo that’s acceptable; for production:

- Put the service behind a VPN or auth proxy.
- Do not commit API keys or secrets to git.

---

## Files in this folder

| File | Purpose |
|------|---------|
| `Dockerfile` | Official `ollama/ollama` image + startup script |
| `start.sh` | Starts server, pulls models |
| `railway.toml` | Railway health check & Docker build |
| `render.yaml` | Render Blueprint config |
