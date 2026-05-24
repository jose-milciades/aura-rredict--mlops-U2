FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV PREDICTIONS_FILE=/app/data/predictions.csv

WORKDIR /app

COPY app.py ./app.py
COPY static ./static

VOLUME ["/app/data"]

EXPOSE 8000

CMD ["python", "app.py"]
