FROM python:3.12-slim

WORKDIR /app
COPY web/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY web/app.py /app/app.py
COPY web/templates /app/templates
COPY web/static /app/static

CMD ["python", "/app/app.py"]
