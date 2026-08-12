#!/bin/bash
set -e

echo "Starting Ollama server on ${OLLAMA_HOST:-0.0.0.0:11434}..."
ollama serve &
SERVE_PID=$!

echo "Waiting for Ollama to become ready..."
for i in $(seq 1 60); do
  if ollama list >/dev/null 2>&1; then
    echo "Ollama is ready."
    break
  fi
  if [ "$i" -eq 60 ]; then
    echo "Ollama did not start in time."
    exit 1
  fi
  sleep 2
done

MODELS=("phi3:mini" "gemma:2b" "moondream" "tinyllama")

for model in "${MODELS[@]}"; do
  echo "Pulling ${model}..."
  if ollama pull "${model}"; then
    echo "Pulled ${model} successfully."
  else
    echo "Warning: failed to pull ${model}. The app may still work with other models."
  fi
done

echo "Model pull complete. Ollama server is running."
wait "${SERVE_PID}"
