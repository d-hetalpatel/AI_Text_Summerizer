FROM python:3.10-slim

WORKDIR /app

# Create a writable directory for Streamlit config
ENV HOME=/app
RUN mkdir -p /app/.streamlit

# Copy requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose Streamlit port
EXPOSE 7860

# Set Streamlit environment variables
ENV STREAMLIT_SERVER_PORT=7860
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Disable telemetry and usage stats (optional)
ENV STREAMLIT_TELEMETRY=False

# Run the app
CMD ["streamlit", "run", "app.py"]
