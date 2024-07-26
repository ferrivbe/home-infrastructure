FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /api

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy psycopg2-binary

# Copy project files
COPY ./src /api/src

# Command to run the application
CMD ["uvicorn", "src.handler:app", "--host", "0.0.0.0", "--port", "8000"]
