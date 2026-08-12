FROM ollama/ollama:latest

# start.sh sets OLLAMA_HOST from $PORT at runtime (Railway injects PORT dynamically).
ENV OLLAMA_ORIGINS=*

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Default Ollama port; Railway maps its public proxy to whatever PORT is set.
EXPOSE 11434

HEALTHCHECK --interval=30s --timeout=10s --start-period=300s --retries=5 \
  CMD curl -sf "http://127.0.0.1:${PORT:-11434}/api/tags" || exit 1

CMD ["/start.sh"]
