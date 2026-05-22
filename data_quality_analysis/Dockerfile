FROM python:3.12-slim

WORKDIR /app
COPY data_quality_analysis/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY data_quality_analysis/app.py /app/app.py

CMD ["python", "/app/app.py"]
