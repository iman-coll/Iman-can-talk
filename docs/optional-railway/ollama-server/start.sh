#!/bin/bash
set -e

# Railway (and other PaaS) inject a dynamic PORT; Ollama must listen on it.
PORT="${PORT:-11434}"
export OLLAMA_HOST="0.0.0.0:${PORT}"
export OLLAMA_ORIGINS="${OLLAMA_ORIGINS:-*}"

echo "Starting Ollama server on ${OLLAMA_HOST} (OLLAMA_ORIGINS=${OLLAMA_ORIGINS})..."
ollama serve &
SERVE_PID=$!

echo "Waiting for Ollama to become ready..."
for i in $(seq 1 90); do
  if curl -sf "http://127.0.0.1:${PORT}/api/tags" >/dev/null 2>&1; then
    echo "Ollama is ready."
    break
  fi
  if ollama list >/dev/null 2>&1; then
    echo "Ollama is ready."
    break
  fi
  if [ "$i" -eq 90 ]; then
    echo "Ollama did not start in time."
    exit 1
  fi
  sleep 2
done

# All models used by the Streamlit app dropdown.
# Set OLLAMA_MODELS=phi3:mini to pull fewer models on low-memory plans.
if [ -n "${OLLAMA_MODELS:-}" ]; then
  IFS=',' read -ra MODELS <<< "${OLLAMA_MODELS}"
else
  MODELS=("phi3:mini" "gemma:2b" "moondream" "tinyllama")
fi

for model in "${MODELS[@]}"; do
  echo "Pulling ${model}..."
  if ollama pull "${model}"; then
    echo "Pulled ${model} successfully."
  else
    echo "Warning: failed to pull ${model}. The app may still work with other models."
  fi
done

echo "Model pull complete. Ollama server is running on port ${PORT}."
wait "${SERVE_PID}"
