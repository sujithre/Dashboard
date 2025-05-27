# Stage 1: Build frontend
FROM node:20-slim as frontend-build
WORKDIR /app
# Copy frontend files
COPY static/js/main.js ./static/js/
COPY templates/index.html ./templates/
# Install Vue.js dependencies (if needed)
RUN npm install vue@next

# Stage 2: Python base with dependencies
FROM python:3.9-slim as build
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 3: Final image
FROM python:3.9-slim
WORKDIR /app

# Copy Python dependencies from build stage
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy frontend files from frontend-build stage
COPY --from=frontend-build /app/static/js/ ./static/js/
COPY --from=frontend-build /app/templates/ ./templates/

# Copy application files
COPY app.py .
COPY Cosrdetails-Feb.csv .

# Create a non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Configure environment
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 8000

# Run the application with gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
