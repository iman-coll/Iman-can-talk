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


def _connection_hint(base_url: str, error: Exception) -> str:
    if _is_streamlit_cloud() and _is_localhost_url(base_url):
        return (
            "This app is running on **Streamlit Cloud**, which cannot reach Ollama on your "
            "PC. Set `OLLAMA_BASE_URL` in **App settings → Secrets** to a remote Ollama server "
            "(for example a VM with Ollama exposed over HTTPS)."
        )

    errno = getattr(error, "errno", None)
    if errno == 99 or "Cannot assign requested address" in str(error):
        return (
            "This often means `localhost` resolved to IPv6 (`::1`) while Ollama listens on "
            "IPv4 only. The app now defaults to `127.0.0.1`; restart Streamlit after pulling "
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


@st.cache_resource(show_spinner=False)
def check_ollama_connection(base_url: str) -> dict:
    """Ping Ollama /api/tags once per server URL per app process."""
    tags_url = f"{base_url}/api/tags"
    try:
        request = urllib.request.Request(tags_url, method="GET")
        with urllib.request.urlopen(request, timeout=5) as response:
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


def _cloud_localhost_misconfiguration(base_url: str) -> str | None:
    if _is_streamlit_cloud() and _is_localhost_url(base_url):
        return (
            "Streamlit Cloud cannot connect to `localhost` or `127.0.0.1` — those addresses "
            "refer to the cloud container, not your computer. Add `OLLAMA_BASE_URL` in "
            "**App settings → Secrets** pointing to a publicly reachable Ollama server."
        )
    return None


# Optional LangSmith tracing
langchain_api_key = _get_setting("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACKING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Imans-Chatbot-Ollama-Models-For-Asking-Questions"

OLLAMA_BASE_URL = _normalize_ollama_url(_get_setting("OLLAMA_BASE_URL", DEFAULT_OLLAMA_URL))

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

cloud_config_error = _cloud_localhost_misconfiguration(OLLAMA_BASE_URL)
connection_status = {"ok": False, "error": "", "hint": ""}
if not cloud_config_error:
    connection_status = check_ollama_connection(OLLAMA_BASE_URL)

ollama_ready = not cloud_config_error and connection_status["ok"]

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Select Open Source Model",
        ["phi3:mini", "gemma:2b", "Moondream", "tinyllama"],
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=300, value=150)
    st.caption(f"Ollama server: `{OLLAMA_BASE_URL}`")
    if _is_streamlit_cloud():
        st.caption("Environment: Streamlit Cloud")
    else:
        st.caption("Environment: Local")

    if cloud_config_error:
        st.error("Misconfigured for cloud")
    elif connection_status["ok"]:
        st.success("Ollama connected")
    else:
        st.error("Ollama unreachable")

if cloud_config_error:
    st.error(cloud_config_error)
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
elif not ollama_ready:
    st.info("Fix the Ollama connection above, then enter a question to get started.")
else:
    st.info("Enter a question above to get started.")
