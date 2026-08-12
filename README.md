# Iman's Ollama Chatbot

A Streamlit chatbot that uses [Ollama](https://ollama.com/) open-source models via LangChain for question answering.

## Features

- Choose from multiple Ollama models (phi3:mini, gemma:2b, Moondream, tinyllama)
- Adjustable temperature and max tokens
- Optional LangSmith tracing for debugging

## Local Setup

1. Install [Ollama](https://ollama.com/download):
   - **Windows:** Download and run the installer from ollama.com. Ollama starts automatically in the system tray.
   - **macOS / Linux:** Follow the install instructions on ollama.com, then start the service if needed:
     ```bash
     ollama serve
     ```

2. Verify Ollama is running:
   ```bash
   ollama --version
   curl http://127.0.0.1:11434/api/tags
   ```

3. Pull a model:
   ```bash
   ollama pull phi3:mini
   ```

4. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. (Optional) Copy `.env.example` to `.env` and adjust settings:
   ```
   OLLAMA_BASE_URL=http://127.0.0.1:11434
   LANGCHAIN_API_KEY=your_langsmith_api_key
   ```
   Use `127.0.0.1` instead of `localhost` to avoid IPv6 connection errors (`Errno 99`).

6. Run the app:
   ```bash
   streamlit run app.py
   ```

The sidebar shows **Ollama connected** when the server is reachable. If not, follow the on-screen guidance before asking questions.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **New app** and select this repository.
4. Set **Main file path** to `app.py`.
5. Add secrets in **App settings → Secrets** (TOML format). **`OLLAMA_BASE_URL` is required on Streamlit Cloud:**
   ```toml
   OLLAMA_BASE_URL = "https://your-remote-ollama-server:11434"
   LANGCHAIN_API_KEY = "your_langsmith_api_key"
   ```
6. Deploy.

> **Important:** Streamlit Cloud cannot reach `localhost` or `127.0.0.1` — those refer to the cloud container, not your PC. Host Ollama on a remote VM or cloud instance, expose its API (HTTPS recommended), and set `OLLAMA_BASE_URL` in secrets. The app detects Streamlit Cloud and shows a clear error if this is missing.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_BASE_URL` | Yes (cloud) | Ollama API URL (default locally: `http://127.0.0.1:11434`) |
| `LANGCHAIN_API_KEY` | No | LangSmith API key for optional tracing |

## Author

**Iman Faisal** ([@iman-coll](https://github.com/iman-coll))
