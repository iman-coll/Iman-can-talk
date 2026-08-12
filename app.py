import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

load_dotenv()


def _get_setting(key: str, default: str = "") -> str:
    """Read config from Streamlit secrets (cloud) or environment variables (local)."""
    try:
        if key in st.secrets:
            return str(st.secrets[key]).strip()
    except Exception:
        pass
    return os.getenv(key, default).strip()


# Optional LangSmith tracing
langchain_api_key = _get_setting("LANGCHAIN_API_KEY")
if langchain_api_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
    os.environ["LANGCHAIN_TRACKING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Imans-Chatbot-Ollama-Models-For-Asking-Questions"

OLLAMA_BASE_URL = _get_setting("OLLAMA_BASE_URL", "http://localhost:11434")

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

with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Select Open Source Model",
        ["phi3:mini", "gemma:2b", "Moondream", "tinyllama"],
    )
    temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=300, value=150)
    st.caption(f"Ollama server: `{OLLAMA_BASE_URL}`")

st.write("🌈 I'm curious! What wonders do you have for me today? 🤔 Ask away! 🌟")
user_input = st.text_input("You: ")

if user_input:
    with st.spinner("Thinking..."):
        try:
            response = generate_response(user_input, model, temperature, max_tokens)
            st.write(response)
        except Exception as exc:
            st.error(
                "Could not reach the Ollama server. Make sure Ollama is running and "
                f"accessible at `{OLLAMA_BASE_URL}`.\n\nDetails: {exc}"
            )
else:
    st.info("Enter a question above to get started.")
