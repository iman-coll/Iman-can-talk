# Free Deploy Guide — After Railway Trial Expires

**For:** [@iman-coll](https://github.com/iman-coll) · Streamlit chatbot + remote Ollama  
**Repo:** [OllamaModel-of-Iman-For-Chatbot](https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot)

Railway’s trial/credits are gone. This guide covers **zero-cost** ways to connect your [Streamlit Community Cloud](https://share.streamlit.io/) app to Ollama via `OLLAMA_BASE_URL`.

---

## START HERE — Free Forever (5 steps)

**Best for you:** Local Ollama on your Windows PC + **ngrok** tunnel.  
**Cost:** $0 forever · **Credit card:** not required · **Time:** ~15 minutes

Your Streamlit app already runs free on [Streamlit Cloud](https://share.streamlit.io/). It just needs a **public HTTPS URL** to reach Ollama on your PC.

| Step | What to do |
|------|------------|
| **1** | Confirm Ollama works: `curl http://127.0.0.1:11434/api/tags` |
| **2** | Install ngrok: `winget install ngrok.ngrok` → sign up free at [dashboard.ngrok.com](https://dashboard.ngrok.com/) → `ngrok config add-authtoken YOUR_TOKEN` |
| **3** | Claim one free static domain: Dashboard → **Cloud Edge → Domains → Create Domain** → e.g. `iman-ollama.ngrok-free.app` |
| **4** | Start tunnel (leave terminal open): `ngrok http 11434 --url=iman-ollama.ngrok-free.app --host-header=localhost:11434` |
| **5** | Streamlit **App settings → Secrets** → paste `OLLAMA_BASE_URL = "https://iman-ollama.ngrok-free.app"` → **Save → Reboot app** |

**Keep running while others use the chatbot:** Ollama (system tray) + the ngrok terminal window + PC awake.

**Quick test only?** Use Cloudflare quick tunnel (no signup, but URL changes every restart) — see [B2a](#b2a--quick-tunnel-5-minutes-url-changes-each-run) below.

**Need 24/7 without your PC on?** See [Option E — Oracle Cloud](#option-e--oracle-cloud-always-free-vm) (free forever, but harder + credit card verification).

Full details, alternatives, and troubleshooting are below.

---

## Which option should I pick?

| Option | Cost | Credit card | Easiest? | Works for Ollama? |
|--------|------|-------------|----------|-------------------|
| **B — Local Ollama + tunnel (ngrok / Cloudflare)** | $0 | No | **Yes — start here** | Yes (uses your PC’s RAM/GPU) |
| **A — Render** | $0 tier exists | Often yes (web services) | Medium | **Unlikely** — free tier is **512 MB RAM**; `phi3:mini` needs ~2.3 GB |
| **C — Fly.io** | Pay-as-you-go | Yes | Medium | **No free tier** for new accounts (2 h / 7 day trial only) |
| **D — Hugging Face Spaces (Docker)** | $0 CPU tier | No | Hard | Tight RAM; slow CPU inference |
| **E — Oracle Cloud Always Free VM** | $0 forever | Yes (verification) | Hard | Yes — 24 GB RAM ARM VM, full cloud Ollama |

### Recommended for you right now

> **Use Option B — expose Ollama on your Windows PC with a free tunnel (ngrok or Cloudflare).**
>
> You already have Ollama installed. No cloud RAM limits, no model re-download in the cloud, no credit card. Streamlit Cloud only needs a public HTTPS URL in secrets.

**Trade-off:** Your PC must stay on, Ollama running, and the tunnel active while others use the chatbot.

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

## Option B — Local Ollama + tunnel (recommended, $0)

Streamlit Cloud runs in the cloud. It cannot reach `127.0.0.1` on your PC. A tunnel gives you a public HTTPS URL that forwards to local port `11434`.

### B1 — ngrok (simplest stable URL, no own domain)

ngrok’s free plan includes **one permanent** `*.ngrok-free.app` subdomain.

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
| ngrok rate limit | Free tier caps requests/bandwidth — use Cloudflare named tunnel or Oracle |

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
