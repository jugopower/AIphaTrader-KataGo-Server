FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \

    PYTHONUNBUFFERED=1 \

    PORT=8000 \

    KATAGO_VERSION=v1.16.5 \

    KATAGO_HOME=/opt/katago \

    KATAGO_BIN=/opt/katago/katago \

    KATAGO_MODEL=/opt/katago/model.bin.gz \

    KATAGO_CONFIG=/app/config/analysis.cfg

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \

    ca-certificates \

    curl \

    unzip \

    libgomp1 \

    libstdc++6 \

    && rm -rf /var/lib/apt/lists/*

# 安裝 Python 套件

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 下載 KataGo CPU Eigen Linux x64

RUN mkdir -p ${KATAGO_HOME} \

    && curl -L \

    "https://github.com/lightvector/KataGo/releases/download/${KATAGO_VERSION}/katago-${KATAGO_VERSION}-eigen-linux-x64.zip" \

    -o /tmp/katago.zip \

    && unzip /tmp/katago.zip -d /tmp/katago \

    && find /tmp/katago -type f -name katago -exec cp {} ${KATAGO_BIN} \; \

    && chmod +x ${KATAGO_BIN} \

    && rm -rf /tmp/katago /tmp/katago.zip

COPY app ./app

COPY config ./config

EXPOSE 8000 

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
