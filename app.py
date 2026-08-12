import os
import socket
import urllib.error
import urllib.request

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

load_dotenv()

DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEPLOY_GUIDE_URL = (
    "https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot"
    "/blob/main/deploy/ollama-server/README.md"
)


def _get_setting(key: str, default: str = "") -> str:
    """Read config from Streamlit secrets (cloud) or environment variables (local)."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, default).strip()


def _is_streamlit_cloud() -> bool:
    """Streamlit Community Cloud runs apps as the 'appuser' Linux user."""
    return os.getenv("USER") == "appuser"


def _normalize_ollama_url(url: str) -> str:
    """Use IPv4 loopback locally to avoid localhost -> ::1 (Errno 99) issues."""
    url = url.strip().rstrip("/")
    if "localhost" in url.lower():
        url = url.replace("localhost", "127.0.0.1").replace("LOCALHOST", "127.0.0.1")
    return url


def _is_localhost_url(url: str) -> bool:
    lowered = url.lower()
    return any(host in lowered for host in ("127.0.0.1", "localhost", "0.0.0.0", "[::1]"))


def _has_cloud_ollama_secret() -> bool:
    try:
        return bool(str(st.secrets.get("OLLAMA_BASE_URL", "")).strip())
    except Exception:
        return False


def _resolve_ollama_url() -> tuple[str, str | None]:
    """
    Return (base_url, cloud_config_error).

    cloud_config_error is one of:
      - "missing_secret" — on Streamlit Cloud with no OLLAMA_BASE_URL in secrets
      - "localhost_on_cloud" — secret points at localhost (invalid on cloud)
      - None — configuration looks fine
    """
    if _is_streamlit_cloud():
        if not _has_cloud_ollama_secret():
            return DEFAULT_OLLAMA_URL, "missing_secret"
        url = _normalize_ollama_url(str(st.secrets["OLLAMA_BASE_URL"]))
        if _is_localhost_url(url):
            return url, "localhost_on_cloud"
        return url, None

    url = _normalize_ollama_url(_get_setting("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL))
    return url, None


def _connection_hint(base_url: str, error: Exception) -> str:
    if _is_streamlit_cloud():
        if _is_localhost_url(base_url):
            return (
                "On Streamlit Cloud, `localhost` and `127.0.0.1` point to the cloud "
                "container — not your PC. Set `OLLAMA_BASE_URL` in **App settings → "
                f"Secrets** to your Railway Ollama URL. See the [deploy guide]({DEPLOY_GUIDE_URL})."
            )
        return (
            f"Check that your remote Ollama server is running and that "
            f"`OLLAMA_BASE_URL` is correct. Test with "
            f"`curl {base_url}/api/tags`. "
            f"Setup help: [deploy guide]({DEPLOY_GUIDE_URL})."
        )

    errno = getattr(error, "errno", None)
    if errno == 99 or "Cannot assign requested address" in str(error):
        return (
            "This often means `localhost` resolved to IPv6 (`::1`) while Ollama listens on "
            "IPv4 only. The app defaults to `127.0.0.1`; restart Streamlit after pulling "
            "the latest code."
        )

    if _is_localhost_url(base_url):
        return (
            "Ollama does not appear to be running locally. Install it from "
            "[ollama.com/download](https://ollama.com/download), then run `ollama serve` "
            "(or start the Ollama app on Windows) and pull a model: `ollama pull phi3:mini`."
        )

    return (
        "Check that the remote Ollama server is running, reachable from this environment, "
        "and that `OLLAMA_BASE_URL` in secrets or `.env` is correct."
    )


def _render_cloud_setup_ui(error_kind: str) -> None:
    st.error("Deploy Ollama server first")
    if error_kind == "missing_secret":
        st.markdown(
            """
This app runs on **Streamlit Cloud**, which cannot run Ollama on your computer or inside
its own container. You need a **remote Ollama server** (free on Railway).

### Setup (~5 minutes)

1. **[Deploy Ollama to Railway](https://github.com/iman-coll/OllamaModel-of-Iman-For-Chatbot/blob/main/deploy/ollama-server/README.md)**  
   Follow the step-by-step guide in `deploy/ollama-server/README.md`.

2. **Copy your Railway public URL**  
   Example: `https://your-app.up.railway.app`

3. **Add Streamlit secrets** — open your app on [share.streamlit.io](https://share.streamlit.io),
   go to **App settings → Secrets**, and paste:

```toml
OLLAMA_BASE_URL = "https://your-app.up.railway.app"
```

4. **Reboot the app** (Manage app → Reboot).

The sidebar will show **Ollama connected** when everything is wired up.
            """
        )
    else:
        st.markdown(
            f"""
`OLLAMA_BASE_URL` in Streamlit secrets must be a **public cloud URL**, not `localhost`
or `127.0.0.1`.

Replace it with your Railway URL, for example:

```toml
OLLAMA_BASE_URL = "https://your-app.up.railway.app"
```

Full instructions: **[Ollama deploy guide]({DEPLOY_GUIDE_URL})**
            """
        )


@st.cache_resource(show_spinner=False)
def check_ollama_connection(base_url: str) -> dict:
    """Ping Ollama /api/tags once per server URL per app process."""
    tags_url = f"{base_url}/api/tags"
    try:
        request = urllib.request.Request(tags_url, method="GET")
        with urllib.request.urlopen(request, timeout=10) as response:
            if response.status == 200:
                return {"ok": True, "error": "", "hint": ""}
            return {
                "ok": False,
                "error": f"Unexpected HTTP status {response.status}",
                "hint": _connection_hint(base_url, Exception(f"HTTP {response.status}")),
            }
    except urllib.error.URLError as exc:
        reason = exc.reason
        if isinstance(reason, socket.gaierror):
            error = f"Address lookup failed: {reason}"
        elif isinstance(reason, OSError):
            error = f"{reason}"
        else:
            error = str(reason or exc)
        return {"ok": False, "error": error, "hint": _connection_hint(base_url, reason or exc)}
    except OSError as exc:
        return {"ok": False, "error": str(exc), "hint": _connection_hint(base_url, exc)}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "hint": _connection_hint(base_url, exc)}


# Optional LangSmith tracing
langchain_api_key = _get_setting("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACKING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Imans-Chatbot-Ollama-Models-For-Asking-Questions"

OLLAMA_BASE_URL, cloud_config_error = _resolve_ollama_url()

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful and informative assistant designed for question answering.
                    Please provide detailed and insightful responses to user queries.
                    If a user asks for help, offer a comprehensive overview of the chatbot's features, including:

                    * **How to ask questions:** Explain how users can phrase their questions effectively. For instance, mention using clear and concise language, and the types of information the bot is best equipped to handle.
                    * **Available commands:** If there are specific keywords or commands, list them and describe their functionality. This could be things like "help," "examples," or any other custom commands you might want to add.
                    * **Supported topics:** Briefly mention the chatbot's knowledge domain. Is it focused on a specific area like data science or general knowledge? This helps users to know what kind of questions to ask.
                    * **Examples:** Provide a few sample questions to demonstrate how to interact with the chatbot effectively.

                    Always be friendly, patient, and aim to provide the most useful information possible.""",
        ),
        ("user", "Question: {question}"),
    ]
)


def generate_response(question: str, model: str, temperature: float, max_tokens: int) -> str:
    llm = OllamaLLM(
        model=model,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        num_predict=max_tokens,
    )
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"question": question})


st.set_page_config(
    page_title="Iman's Ollama Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("Imans-Chatbot-Ollama-Models-For-Asking-Questions")

connection_status = {"ok": False, "error": "", "hint": ""}
if cloud_config_error in ("missing_secret", "localhost_on_cloud"):
    ollama_ready = False
elif cloud_config_error is None:
    connection_status = check_ollama_connection(OLLAMA_BASE_URL)
    ollama_ready = connection_status["ok"]
else:
    ollama_ready = False

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Select Open Source Model",
        ["phi3:mini", "gemma:2b", "moondream", "tinyllama"],
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=300, value=150)
    st.caption(f"Ollama server: `{OLLAMA_BASE_URL}`")
    if _is_streamlit_cloud():
        st.caption("Environment: Streamlit Cloud")
    else:
        st.caption("Environment: Local")

    if cloud_config_error in ("missing_secret", "localhost_on_cloud"):
        st.error("Remote Ollama not configured")
    elif connection_status["ok"]:
        st.success("Ollama connected")
    else:
        st.error("Ollama unreachable")

if cloud_config_error in ("missing_secret", "localhost_on_cloud"):
    _render_cloud_setup_ui(cloud_config_error)
elif not connection_status["ok"]:
    st.warning(
        f"Could not reach Ollama at `{OLLAMA_BASE_URL}`.\n\n"
        f"**Details:** {connection_status['error']}\n\n"
        f"{connection_status['hint']}"
    )

st.write("🌈 I'm curious! What wonders do you have for me today? 🤔 Ask away! 🌟")
user_input = st.text_input("You: ", disabled=not ollama_ready)

if user_input and ollama_ready:
    with st.spinner("Thinking..."):
        try:
            response = generate_response(user_input, model, temperature, max_tokens)
            st.write(response)
        except Exception as exc:
            st.error(
                f"Could not reach the Ollama server at `{OLLAMA_BASE_URL}`.\n\n"
                f"**Details:** {exc}\n\n"
                f"{_connection_hint(OLLAMA_BASE_URL, exc)}"
            )
elif not ollama_ready and cloud_config_error not in ("missing_secret", "localhost_on_cloud"):
    st.info("Fix the Ollama connection above, then enter a question to get started.")
elif ollama_ready:
    st.info("Enter a question above to get started.")
