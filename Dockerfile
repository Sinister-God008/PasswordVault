FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY SecurePass/ ./SecurePass/
COPY run.py .

ENV PORT=5000
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["python", "run.py"]
