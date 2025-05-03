FROM python:3.12-bookworm AS build

# Environment settings for clean, safe builds
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=true \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    QR_CODE_DIR=/myapp/qr_codes

# Set working directory
WORKDIR /tmp

# Install only build-time packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev

# Copy and install requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install -r requirements.txt


FROM python:3.12-slim-bookworm AS runtime

# Upgrade system packages to patch OS CVEs (libc, openssl, etc.)
RUN apt-get update && \
    apt-get -y upgrade --no-install-recommends && \
    apt-get -y install --no-install-recommends libc-bin && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from build stage
COPY --from=build /install /usr/local

# Set environment variables again in runtime container
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PATH="/usr/local/bin:$PATH" \
    QR_CODE_DIR=/myapp/qr_codes

# Set the working directory for the runtime
WORKDIR /myapp

# Create non-root user and switch
RUN useradd -m myuser
USER myuser

# Copy the application code with correct ownership
COPY --chown=myuser:myuser . .

# Expose port 8000 to run FastAPI
EXPOSE 8000

# Entrypoint: run FastAPI with uvicorn
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
