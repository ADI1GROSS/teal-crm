FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpango1.0-dev \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libgdk-pixbuf-2.0-dev \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV WEASYPRINT_CAIRO_CFF=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "tealcrm.wsgi:application", "--bind", "0.0.0.0:8000", "--timeout", "120"]
