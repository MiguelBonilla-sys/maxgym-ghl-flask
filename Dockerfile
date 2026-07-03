FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY templates /app/templates/
COPY screenshots /app/screenshots/
COPY research /app/research/
COPY assets /app/assets/

EXPOSE 5000

CMD ["python", "app.py"]
