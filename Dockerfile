FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install git-lfs and download large assets from GitHub
RUN apt-get update && apt-get install -y --no-install-recommends git-lfs && \
    git lfs install && \
    rm -rf /var/lib/apt/lists/*

# Clone repo with full LFS content
RUN git clone --depth=1 https://github.com/MiguelBonilla-sys/maxgym-ghl-flask.git /repo_tmp && \
    cd /repo_tmp && git lfs pull && \
    cp -r screenshots /app/ && \
    cp -r research /app/ && \
    cp -r assets /app/ && \
    rm -rf /repo_tmp

# Copy app source
COPY app.py .
COPY templates /app/templates/

EXPOSE 5000

CMD ["python", "app.py"]
