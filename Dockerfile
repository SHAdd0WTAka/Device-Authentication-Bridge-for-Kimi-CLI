FROM python:3.11-slim

LABEL org.opencontainers.image.source="https://github.com/SHAdd0WTAka/Device-Authentication-Bridge-for-Kimi-CLI"
LABEL org.opencontainers.image.description="Device Authentication Bridge for Kimi CLI"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src/ ./src/

RUN pip install -e .

CMD ["python", "-c", "from kimi_auth_bridge import KimiAuthBridge; print('Kimi Auth Bridge loaded successfully')"]
