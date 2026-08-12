# Easiest Deploy Guide — Iman Faisal (@iman-coll)

Follow these steps in order. Total time: ~15 minutes of clicking, plus 20–40 minutes waiting for models on Railway.

---

## Step 1 — Railway (Ollama server with all 4 models)

1. Open **[railway.app](https://railway.app/)** → sign in with **GitHub** (`iman-coll`).
2. Click **New Project** → **Deploy from GitHub repo**.
3. Choose **`iman-coll/OllamaModel-of-Iman-For-Chatbot`**.
4. Click the new service → **Settings**:
   - **Root Directory:** `deploy/ollama-server`
5. **Settings → Networking → Generate Domain** → copy your URL, e.g.  
   `https://ollama-chatbot-production.up.railway.app`
6. Open **Deployments → View Logs** and wait until you see:  
   `Model pull complete. Ollama server is running.`
7. **Test:** open in browser:  
   `https://YOUR-URL.up.railway.app/api/tags`  
   You should see JSON listing `phi3:mini`, `gemma:2b`, `moondream`, `tinyllama`.

> **Tip:** First deploy downloads ~5 GB of models. Upgrade Railway plan or set env var `OLLAMA_MODELS=phi3:mini` if you run out of memory.

---

## Step 2 — Streamlit (chat UI)

1. Open this link (pre-filled for your repo):  
   **https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py**
2. Sign in with **GitHub** (`iman-coll`) → click **Deploy**.
3. After deploy, go to **App settings → Secrets** and paste (use your Railway URL):

```toml
OLLAMA_BASE_URL = "https://YOUR-URL.up.railway.app"
```

4. Click **Save** → **Manage app → Reboot app**.

---

## Step 3 — Chat!

1. Open your Streamlit app URL (shown on the deploy page).
2. Sidebar should say **Ollama connected**.
3. Pick any model: `phi3:mini`, `gemma:2b`, `moondream`, or `tinyllama`.
4. Type a question and press Enter.

---

## Local testing (optional)

If Ollama is installed on your PC:

```powershell
ollama pull phi3:mini
ollama pull gemma:2b
ollama pull moondream
ollama pull tinyllama
cd "D:\AI Projects iman\OllamaModel-of-Iman-For-Chatbot"
py -3 -m streamlit run app.py
```

No secrets needed locally — uses `http://127.0.0.1:11434` automatically.

---

## Quick links

| What | URL |
|------|-----|
| GitHub repo | https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot |
| Railway | https://railway.app/ |
| Streamlit deploy | https://share.streamlit.io/deploy?repository=iman-coll/OllamaModel-of-Iman-For-Chatbot&branch=main&mainModule=app.py |
| Ollama deploy details | [deploy/ollama-server/README.md](deploy/ollama-server/README.md) |

---

**Author:** Iman Faisal · [@iman-coll](https://github.com/iman-coll)
