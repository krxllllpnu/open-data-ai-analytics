FROM python:3.12-slim

WORKDIR /app
COPY visualization/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY visualization/app.py /app/app.py

CMD ["python", "/app/app.py"]
