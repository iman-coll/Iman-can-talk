# Free Deploy Guide — After Railway Trial Expires

**For:** [@iman-coll](https://github.com/iman-coll) · Streamlit chatbot + Ollama  
**Repo:** [OllamaModel-of-Iman-For-Chatbot](https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot)

Railway’s trial/credits are gone. **ngrok now pushes paid plans** for many users. This guide covers **100% free** paths — no payment, no credit card.

---

## NO PAYMENT / NO NGROK — START HERE

**Pick one path in 10 seconds:**

| I want… | Use | Payment? | Time |
|---------|-----|----------|------|
| **Chatbot working RIGHT NOW on my PC** | **[Option 1 — Local Streamlit](#option-1--local-streamlit-simplest-100-free)** | **Never** | **~2 min** |
| **Public URL on share.streamlit.io** | **[Option 2 — Cloudflare Quick Tunnel](#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud)** | **Never** | **~10 min** |
| **Cloud Ollama without my PC on** | [Option 3 — HF Spaces](#option-3--hugging-face-spaces-not-recommended) or [Oracle Cloud](#option-e--oracle-cloud-always-free-vm) | Never (Oracle needs card verify) | Hard |

---

### Option 1 — Local Streamlit (simplest, 100% free)

**Best if you just want the chatbot working.** GitHub stores your code (free). Ollama runs on your PC. No tunnel, no signup, no payment.

#### Copy-paste — Windows (PowerShell)

```powershell
# 1. Go to your project folder (clone from GitHub if needed)
cd "D:\AI Projects iman\OllamaModel-of-Iman-For-Chatbot"

# 2. Confirm Ollama is running (system tray icon)
curl http://127.0.0.1:11434/api/tags

# 3. Pull a model if you haven't yet
ollama pull phi3:mini

# 4. Install Python deps (once)
py -3 -m pip install -r requirements.txt

# 5. Run the chatbot — browser opens automatically
py -3 -m streamlit run app.py
```

**Done.** Chat at `http://localhost:8501`. Sidebar should show **Ollama connected**.

No `OLLAMA_BASE_URL` needed — the app defaults to `http://127.0.0.1:11434`.

#### Phone on same Wi‑Fi (optional)

Find your PC’s local IP (`ipconfig` → IPv4, e.g. `192.168.1.42`), then:

```powershell
py -3 -m streamlit run app.py --server.address 0.0.0.0
```

On your phone’s browser: `http://192.168.1.42:8501` (replace with your IP).

**Keep running:** Ollama (tray) + the Streamlit terminal. PC must stay awake.

---

### Option 2 — Cloudflare Quick Tunnel (free for Streamlit Cloud)

**Best if you need the app on [share.streamlit.io](https://share.streamlit.io/)** and want **zero payment forever.**

Streamlit Cloud runs in the cloud — it cannot reach `127.0.0.1` on your PC. Cloudflare’s **quick tunnel** gives a free public `https://….trycloudflare.com` URL with **no account, no credit card, no payment**.

> **Trade-off:** The URL **changes every time** you restart the tunnel. Update Streamlit secrets after each restart. For a stable URL without paying, use [Cloudflare named tunnel](#b2b--named-tunnel-stable-url-needs-free-cloudflare-account--domain) (free account + domain) or [Option 1](#option-1--local-streamlit-simplest-100-free).

#### Copy-paste — Windows (two terminals)

**Terminal 1 — Ollama** (usually already running from system tray):

```powershell
curl http://127.0.0.1:11434/api/tags
```

**Terminal 2 — Install cloudflared (once), then start tunnel:**

```powershell
winget install Cloudflare.cloudflared
cloudflared tunnel --url http://localhost:11434 --http-host-header="localhost:11434"
```

Wait for output like:

```
Your quick Tunnel has been created! Visit it at:
https://random-words-here.trycloudflare.com
```

**Test the URL** (new terminal or browser):

```powershell
curl https://random-words-here.trycloudflare.com/api/tags
```

You should see JSON listing your models.

**Streamlit Cloud secrets** — [open your app](https://share.streamlit.io/) → **App settings → Secrets**:

```toml
OLLAMA_BASE_URL = "https://random-words-here.trycloudflare.com"
```

Click **Save → Reboot app**. Sidebar: **Ollama connected**.

**Keep running while others use the chatbot:** Ollama (tray) + cloudflared terminal + PC awake.

---

### Option 3 — Hugging Face Spaces (not recommended)

| Approach | Feasible? | Why not easiest |
|----------|-----------|-----------------|
| **Docker Space running Ollama** | Possible | Free CPU tier is slow; model pulls take long; RAM tight for multiple models; cold starts |
| **Hugging Face Inference API** | **No** | Not a drop-in Ollama replacement — different API, different models |
| **Deploy Streamlit on HF Spaces** | Possible | Still needs a **remote Ollama URL** — same tunnel problem |

**Verdict:** HF Spaces is viable for experiments only. For **right now**, use [Option 1](#option-1--local-streamlit-simplest-100-free) or [Option 2](#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud). For **24/7 cloud Ollama**, see [Oracle Cloud](#option-e--oracle-cloud-always-free-vm).

Rough HF flow (if you insist): create a [Docker Space](https://huggingface.co/new-space) → point to `deploy/ollama-server/Dockerfile` → set `OLLAMA_MODELS=phi3:mini` → use Space URL as `OLLAMA_BASE_URL`. Expect slow CPU inference.

---

## Which option should I pick? (full comparison)

| Option | Cost | Credit card | Easiest? | Works for Ollama? |
|--------|------|-------------|----------|-------------------|
| **1 — Local Streamlit** | $0 | No | **Yes — start here** | Yes (PC RAM/GPU) |
| **2 — Cloudflare quick tunnel + Streamlit Cloud** | $0 | No | Easy | Yes (PC must stay on) |
| **B — ngrok tunnel** | May require **paid plan** | Sometimes | Was easy | Yes — [see B1](#b1--ngrok-may-require-payment) |
| **A — Render** | $0 tier exists | Often yes | Medium | **Unlikely** — free tier **512 MB RAM**; `phi3:mini` needs ~2.3 GB |
| **C — Fly.io** | Pay-as-you-go | Yes | Medium | **No free tier** for new accounts |
| **D — Hugging Face Spaces** | $0 CPU tier | No | Hard | Slow; tight RAM |
| **E — Oracle Cloud Always Free VM** | $0 forever | Yes (verification) | Hard | Yes — 24 GB RAM ARM VM |

### Recommended for you right now

> **Just want it working? → [Option 1 — Local Streamlit](#option-1--local-streamlit-simplest-100-free)** (`py -3 -m streamlit run app.py`)
>
> **Need share.streamlit.io public link? → [Option 2 — Cloudflare Quick Tunnel](#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud)** (free forever, no ngrok)

---

## Prerequisites (all options)

1. **Streamlit app** deployed at [share.streamlit.io](https://share.streamlit.io/) from this repo (`app.py`).
2. **Models pulled locally** (at minimum):

   ```powershell
   ollama pull phi3:mini
   ollama pull gemma:2b
   ollama pull moondream
   ollama pull tinyllama
   ```

3. **Test local Ollama:**

   ```powershell
   curl http://127.0.0.1:11434/api/tags
   ```

---

## Option B — Local Ollama + tunnel (for Streamlit Cloud)

Streamlit Cloud runs in the cloud. It cannot reach `127.0.0.1` on your PC. A tunnel gives you a public HTTPS URL that forwards to local port `11434`.

**Prefer Cloudflare (free, no payment):** [Option 2 above](#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud) or [B2 below](#b2--cloudflare-tunnel-free-no-credit-card-for-quick-test).

### B1 — ngrok (may require payment)

> **Note:** ngrok has tightened free-tier limits and may ask for a **paid plan** or credit card. If ngrok blocks you, skip it — use **[Cloudflare Quick Tunnel](#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud)** or **[Local Streamlit](#option-1--local-streamlit-simplest-100-free)** instead.

ngrok’s free plan (when available) includes **one permanent** `*.ngrok-free.app` subdomain.

#### Step 1 — Install ngrok (Windows)

1. Download from [ngrok.com/download](https://ngrok.com/download) or:

   ```powershell
   winget install ngrok.ngrok
   ```

2. Sign up at [dashboard.ngrok.com](https://dashboard.ngrok.com/) (free).

3. Copy your authtoken from the dashboard, then:

   ```powershell
   ngrok config add-authtoken YOUR_AUTHTOKEN
   ```

#### Step 2 — Claim a free static domain

1. In the ngrok dashboard: **Cloud Edge → Domains → Create Domain**.
2. Pick a name, e.g. `iman-ollama` → you get `https://iman-ollama.ngrok-free.app`.

#### Step 3 — Start Ollama (if not already running)

Ollama on Windows usually runs from the system tray after install. Verify:

```powershell
curl http://127.0.0.1:11434/api/tags
```

#### Step 4 — Start the tunnel

Ollama rejects requests whose `Host` header is not `localhost`. Rewrite it:

```powershell
ngrok http 11434 --url=iman-ollama.ngrok-free.app --host-header=localhost:11434
```

Leave this terminal open. Test from another device or [ngrok’s online request tool]:

```powershell
curl https://iman-ollama.ngrok-free.app/api/tags
```

You should see JSON listing your models.

#### Step 5 — Set Streamlit secrets

**App settings → Secrets:**

```toml
OLLAMA_BASE_URL = "https://iman-ollama.ngrok-free.app"
```

**Save → Reboot app.** Sidebar should show **Ollama connected**.

#### ngrok free limits

- ~20k HTTP requests / month
- 1 GB bandwidth / month  
- Fine for personal demos; upgrade if you hit limits

---

### B2 — Cloudflare Tunnel (free, no credit card for quick test)

Two sub-paths: **quick tunnel** (no account, URL changes) vs **named tunnel** (stable URL, needs free Cloudflare account + domain).

#### B2a — Quick tunnel (5 minutes, URL changes each run)

Good for a one-off test. **Not** for long-term Streamlit secrets (URL changes when you restart).

1. Install cloudflared:

   ```powershell
   winget install Cloudflare.cloudflared
   ```

2. Start Ollama locally (tray app or `ollama serve`).

3. Run:

   ```powershell
   cloudflared tunnel --url http://localhost:11434 --http-host-header="localhost:11434"
   ```

4. Copy the `https://….trycloudflare.com` URL from the output.

5. Paste into Streamlit secrets:

   ```toml
   OLLAMA_BASE_URL = "https://YOUR-RANDOM.trycloudflare.com"
   ```

6. Reboot the Streamlit app.

#### B2b — Named tunnel (stable URL, recommended if you use Cloudflare)

Requires a **domain on Cloudflare** (you can transfer an existing domain or register one elsewhere and point nameservers to Cloudflare).

1. **Install cloudflared** (same as above).

2. **Log in:**

   ```powershell
   cloudflared tunnel login
   ```

   A browser opens — pick your Cloudflare account and hostname zone.

3. **Create a tunnel:**

   ```powershell
   cloudflared tunnel create iman-ollama
   ```

   Note the tunnel UUID printed.

4. **Create config file** at `%USERPROFILE%\.cloudflared\config.yml`:

   ```yaml
   tunnel: iman-ollama
   credentials-file: C:\Users\YOUR_USERNAME\.cloudflared\TUNNEL-UUID.json

   ingress:
     - hostname: ollama.yourdomain.com
       service: http://localhost:11434
       originRequest:
         httpHostHeader: localhost:11434
     - service: http_status:404
   ```

   Replace `YOUR_USERNAME`, `TUNNEL-UUID`, and `ollama.yourdomain.com`.

5. **Route DNS:**

   ```powershell
   cloudflared tunnel route dns iman-ollama ollama.yourdomain.com
   ```

6. **Run the tunnel:**

   ```powershell
   cloudflared tunnel run iman-ollama
   ```

7. **Test:**

   ```powershell
   curl https://ollama.yourdomain.com/api/tags
   ```

8. **Streamlit secrets:**

   ```toml
   OLLAMA_BASE_URL = "https://ollama.yourdomain.com"
   ```

#### Run Cloudflare tunnel on Windows startup (optional)

Install as a service so reboots do not break the chatbot:

```powershell
cloudflared service install
```

If the service exits immediately, set an explicit command in Windows Services for `cloudflared` pointing to your `config.yml` and `tunnel run iman-ollama` (see [Cloudflare local tunnel docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/configure-tunnels/local-management/)).

#### Security note

Your Ollama API is **public** without auth. For a class/demo that is usually OK. For production, add [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/policies/access/) or keep the tunnel URL private.

---

## Option A — Render (existing `render.yaml`)

This repo already includes [`deploy/ollama-server/render.yaml`](deploy/ollama-server/render.yaml). Render is a good platform, but the **free web service is 512 MB RAM** — too small for `phi3:mini` (~2.3 GB). Expect OOM crashes unless you upgrade instance size.

Use Render only if you can accept **paid** Standard ($25/mo, 2 GB) or treat free tier as a learning deploy with **no models** (not useful for this chatbot).

### Steps (if you still want to try)

1. Go to [render.com](https://render.com/) → sign up (GitHub login).
2. **New → Blueprint** (or **New Web Service**).
3. Connect repo **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**.
4. Set **Root Directory:** `deploy/ollama-server`.
5. Render reads `render.yaml`:
   - Runtime: Docker
   - Plan: free
   - Health check: `/api/tags`
6. Add environment variable (optional, reduces memory):

   ```
   OLLAMA_MODELS=phi3:mini
   ```

7. Deploy → wait for logs: `Model pull complete. Ollama server is running.`
8. Copy your `https://….onrender.com` URL.
9. Streamlit secrets:

   ```toml
   OLLAMA_BASE_URL = "https://YOUR-SERVICE.onrender.com"
   ```

### Render free-tier behavior

- Spins down after **~15 minutes** with no traffic
- First request after sleep: **30–60+ seconds** cold start
- 750 free instance hours / month

---

## Option C — Fly.io (not free for new users)

Fly.io removed the always-free tier for new accounts. New signups get a **2-hour / 7-day trial**, then pay-as-you-go (~$2+/month minimum for a tiny VM).

Not recommended when Railway trial already expired and you need $0 hosting.

If you still want Fly.io later, you would add a `fly.toml` under `deploy/ollama-server/`, deploy a Docker app, and set `OLLAMA_ORIGINS=*`. See [fly.io/docs](https://fly.io/docs/).

---

## Option D — Hugging Face Spaces (Docker)

[Hugging Face Spaces](https://huggingface.co/spaces) supports Docker and is free on CPU.

- **Pros:** No PC must stay on; git-based deploy.
- **Cons:** CPU inference is slow; free hardware has limited RAM; cold starts; more setup than a tunnel.

Rough flow: create a Space → select Docker → point to `deploy/ollama-server/Dockerfile` → set `OLLAMA_MODELS=phi3:mini` → use the Space URL as `OLLAMA_BASE_URL`. Viable for experiments, not the easiest path.

---

## Option E — Oracle Cloud Always Free VM

Oracle’s **Always Free** tier includes ARM Ampere VMs (up to **4 OCPU / 24 GB RAM**) — enough to run all four chatbot models in the cloud, $0/month if you stay within free limits.

- **Pros:** Real cloud server; PC can be off; stable public IP.
- **Cons:** Sign-up friction; credit card verification; Linux setup (Docker, firewall, systemd).

High-level steps:

1. Create account at [cloud.oracle.com](https://cloud.oracle.com/) → create an **Ampere A1** instance (Ubuntu).
2. Open port **11434** in the instance security list / NSG (restrict to your IP if possible).
3. SSH in → install Docker → clone this repo → build `deploy/ollama-server`.
4. Run container with `-p 11434:11434` and `OLLAMA_ORIGINS=*`.
5. Use `http://YOUR_PUBLIC_IP:11434` or put nginx/Caddy in front for HTTPS.
6. Set `OLLAMA_BASE_URL` in Streamlit secrets (HTTPS strongly preferred).

Best when you need **24/7 cloud Ollama** without paying and without keeping a Windows PC online.

---

## Connect Streamlit (all options)

Deploy or open your app:

**https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py**

**App settings → Secrets** (replace with your tunnel or cloud URL):

```toml
OLLAMA_BASE_URL = "https://your-public-ollama-url"
```

**Save → Manage app → Reboot app.**

Verify sidebar: **Ollama connected**. Send a test message with `phi3:mini`.

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| Streamlit says “Deploy Ollama server first” | Add `OLLAMA_BASE_URL` in secrets and reboot |
| `403` from Ollama through tunnel | Add `--host-header=localhost:11434` (ngrok) or `httpHostHeader: localhost:11434` (Cloudflare) |
| Connection refused | Ollama not running — start tray app; run `curl http://127.0.0.1:11434/api/tags` |
| Tunnel works locally but Streamlit fails | Tunnel process stopped or PC asleep — restart tunnel |
| Render deploy OOM | Free 512 MB too small — use local tunnel (Option B) or Oracle (Option E) |
| ngrok asks for payment | Use [Option 1 — Local Streamlit](#option-1--local-streamlit-simplest-100-free) or [Option 2 — Cloudflare](#option-2--cloudflare-quick-tunnel-free-for-streamlit-cloud) instead |
| ngrok rate limit | Use Cloudflare named tunnel or Oracle |

---

## Quick links

| What | URL |
|------|-----|
| This guide | [DEPLOY-STEPS-FREE.md](DEPLOY-STEPS-FREE.md) |
| Original Railway guide | [DEPLOY-STEPS.md](DEPLOY-STEPS.md) |
| Ollama server folder | [deploy/ollama-server/README.md](deploy/ollama-server/README.md) |
| Streamlit deploy | [share.streamlit.io deploy link](https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py) |
| ngrok dashboard | [dashboard.ngrok.com](https://dashboard.ngrok.com/) |
| Cloudflare Tunnel docs | [developers.cloudflare.com/cloudflare-one/connections/connect-networks](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/) |

---

**Author:** Iman Faisal · [@iman-coll](https://github.com/iman-coll)
