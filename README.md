# Iman's Ollama Chatbot

A Streamlit chatbot that uses [Ollama](https://ollama.com/) open-source models via LangChain for question answering.

## Features

- Choose from multiple Ollama models (phi3:mini, gemma:2b, Moondream, tinyllama)
- Adjustable temperature and max tokens
- Optional LangSmith tracing for debugging

## Local Setup

1. Install [Ollama](https://ollama.com/download) and pull a model:
   ```bash
   ollama pull phi3:mini
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file for LangSmith tracing:
   ```
   LANGCHAIN_API_KEY=your_langsmith_api_key
   OLLAMA_BASE_URL=http://localhost:11434
   ```

4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **New app** and select this repository.
4. Set **Main file path** to `app.py`.
5. Add secrets in **Advanced settings → Secrets** (TOML format):
   ```toml
   LANGCHAIN_API_KEY = "your_langsmith_api_key"
   OLLAMA_BASE_URL = "https://your-remote-ollama-server:11434"
   ```
6. Deploy.

> **Note:** Streamlit Cloud cannot reach `localhost`. You must host Ollama on a remote server (VM, cloud instance, etc.) and set `OLLAMA_BASE_URL` to that address in Streamlit secrets.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OLLAMA_BASE_URL` | No | Ollama API URL (default: `http://localhost:11434`) |
| `LANGCHAIN_API_KEY` | No | LangSmith API key for optional tracing |

## Author

**Iman Faisal** ([@iman-coll](https://github.com/iman-coll))
