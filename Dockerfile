FROM python:3.13-slim

WORKDIR /app

# Install Chromium and its matching driver
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Configure Selenium to use Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PYTHONUNBUFFERED=1
ENV NLTK_DATA=/usr/share/nltk_data

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK tokenizer data
RUN python -c "import nltk; nltk.download('punkt_tab', download_dir='/usr/share/nltk_data')"

# Copy application
COPY app/ ./app/

EXPOSE 7000

# Start the API automatically
CMD ["python", "-m", "app.main"]
