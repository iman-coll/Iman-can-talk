# Free Ollama Setup (Appendix)

**For:** Streamlit Cloud users who need a **free** public Ollama URL.  
**Main deploy guide:** [STREAMLIT-DEPLOY.md](STREAMLIT-DEPLOY.md)

Streamlit Cloud runs in the cloud — it cannot reach `127.0.0.1` on your PC. These paths cost **$0** and need no credit card.

---

## Run locally (no Streamlit Cloud)

**Best if you just want the chatbot working on your PC.** No tunnel, no secrets.

```powershell
cd "D:\AI Projects iman\OllamaModel-of-Iman-For-Chatbot"
curl http://127.0.0.1:11434/api/tags
ollama pull phi3:mini
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run app.py
```

Open `http://localhost:8501`. Sidebar: **Ollama connected**. No `OLLAMA_BASE_URL` needed.

Pull all models: `.\pull-all-models.ps1`

---

## Cloudflare quick tunnel (for Streamlit Cloud)

**Best free path for [share.streamlit.io](https://share.streamlit.io/).**  
Gives a public `https://….trycloudflare.com` URL with **no account and no payment**.

> **Trade-off:** The URL **changes every time** you restart the tunnel. Update Streamlit secrets after each restart.

### Step 1 — Confirm Ollama is running

```powershell
curl http://127.0.0.1:11434/api/tags
```

### Step 2 — Start the tunnel (new terminal)

```powershell
winget install Cloudflare.cloudflared
cloudflared tunnel --url http://localhost:11434 --http-host-header="localhost:11434"
```

Copy the URL from output, e.g. `https://random-words-here.trycloudflare.com`.

### Step 3 — Test

```powershell
curl https://random-words-here.trycloudflare.com/api/tags
```

You should see JSON listing your models.

### Step 4 — Streamlit secrets

[Open your app](https://share.streamlit.io/) → **App settings → Secrets**:

```toml
OLLAMA_BASE_URL = "https://random-words-here.trycloudflare.com"
```

**Save → Reboot app.** Sidebar: **Ollama connected**.

**Keep running while others use the chatbot:** Ollama (tray) + cloudflared terminal + PC awake.

### Stable URL (optional)

For a URL that does not change on restart, use a **named Cloudflare tunnel** with a domain on Cloudflare. See [Cloudflare tunnel docs](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/).

---

## Troubleshooting

| Problem | Fix |
|--------|-----|
| “Deploy Ollama server first” in app | Add `OLLAMA_BASE_URL` in Streamlit secrets and reboot |
| `403` through tunnel | Use `--http-host-header="localhost:11434"` with cloudflared |
| Connection refused | Start Ollama (tray app); test `curl http://127.0.0.1:11434/api/tags` |
| Tunnel works locally but Streamlit fails | Tunnel stopped or PC asleep — restart cloudflared |

---

## Optional paid cloud Ollama

Railway, Render, and similar hosts are **not required**. If you prefer paid cloud hosting instead of a tunnel, see [docs/optional-railway/README.md](docs/optional-railway/README.md).

---

**Author:** Iman Faisal · [@iman-coll](https://github.com/iman-coll)
