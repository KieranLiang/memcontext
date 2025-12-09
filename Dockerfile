FROM python:3.10-slim
WORKDIR /app
COPY memcontext-pypi/ ./memcontext-pypi/
RUN pip install --no-cache-dir -r memcontext-pypi/requirements.txt && \
    apt-get update && \
    apt-get install -y vim && \
    rm -rf /var/lib/apt/lists/*