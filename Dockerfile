# syntax=docker/dockerfile:1

FROM python:3.13-slim
LABEL maintainer = "inspiremirnal@yahoo.com"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]

