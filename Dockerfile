# Django Backend Only (API)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set build-time environment variables (only for build, will be overridden by Render at runtime)
ARG DJANGO_SECRET_KEY=build-time-secret-key-do-not-use-in-production
ARG DJANGO_DEBUG=0
ARG DJANGO_ALLOWED_HOSTS=*
ARG DJANGO_HTTPS=0
ARG DJANGO_CSRF_TRUSTED_ORIGINS=

ENV DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
ENV DJANGO_DEBUG=${DJANGO_DEBUG}
ENV DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}
ENV DJANGO_HTTPS=${DJANGO_HTTPS}
ENV DJANGO_CSRF_TRUSTED_ORIGINS=${DJANGO_CSRF_TRUSTED_ORIGINS}

# Copy Django project
COPY . .

# Create media directory
RUN mkdir -p media staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "90"]
