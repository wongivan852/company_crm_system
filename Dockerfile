# Multi-stage build for security and smaller image size
FROM python:3.11-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    postgresql-dev \
    musl-dev \
    libffi-dev

# Set work directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --user -r requirements.txt

# Final stage with minimal Alpine Linux
FROM python:3.11-alpine

# Install runtime dependencies only
RUN apk add --no-cache \
    postgresql-client \
    libpq \
    && addgroup -g 1000 crm \
    && adduser -D -s /bin/sh -u 1000 -G crm crm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV PATH=/home/crm/.local/bin:$PATH

# Set work directory
WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /root/.local /home/crm/.local

# Copy project files
COPY --chown=crm:crm . /app/

# Create necessary directories with proper permissions
RUN mkdir -p /app/logs /app/static /app/media \
    && chown -R crm:crm /app

# Switch to non-root user
USER crm

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/ || exit 1

# Run the application
CMD ["gunicorn", "crm_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120"]
