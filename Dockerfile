# Dockerfile for the AutoQuizzer Streamlit application.
# Packages the app and its ChromaDB into a self-contained image.
# The GOOGLE_API_KEY must be supplied at runtime — it is never baked into the image.
#
# Build:
#   docker build -t autoquizzer .
#
# Run:
#   docker run -p 8501:8501 -e GOOGLE_API_KEY=<your_key> autoquizzer
#
# To use an external ChromaDB directory instead of the one baked into the image:
#   docker run -p 8501:8501 -e GOOGLE_API_KEY=<your_key> \
#       -v /path/to/Database:/app/Database autoquizzer

# --- Base image ---
FROM python:3.11-slim

# --- Working directory ---
WORKDIR /app

# --- Dependencies ---
# Copy requirements first so this layer is cached unless requirements change
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Application source ---
COPY . .

# --- Runtime configuration ---
EXPOSE 8501

# Streamlit healthcheck — confirms the app is serving before Docker marks it healthy
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# --- Entrypoint ---
CMD ["streamlit", "run", "Frontend/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
