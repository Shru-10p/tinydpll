# Build stage for C++ solver
FROM gcc:11 as builder

WORKDIR /app

# Copy source files
COPY include/ include/
COPY src/ src/
COPY Makefile Makefile

# Build the solver
RUN make

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for Flask and any compiled extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy built binary from builder
COPY --from=builder /app/build/tinydpll build/tinydpll

# Copy Python files
COPY requirements.txt requirements.txt
COPY scripts/ scripts/
COPY web/ web/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=web/app.py
ENV PYTHONUNBUFFERED=1

# Run Flask app
CMD ["python", "web/app.py"]
