# 🐳 Radhe Guardian Bot - Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copy all files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command
CMD ["python", "bot.py"]h
