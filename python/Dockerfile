FROM python:3.13-slim

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser && \
    mkdir /app && \
    chown appuser:appgroup /app

WORKDIR /app

COPY requirements.txt .

RUN apt-get update \
	&& apt-get install -y libpq-dev gcc \
	&& rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]

HEALTHCHECK --interval=20s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1