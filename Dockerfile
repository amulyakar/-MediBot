
# Use Python 3.13 as the base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from creating cache files
ENV PYTHONDONTWRITEBYTECODE=1

# Display Python output immediately
ENV PYTHONUNBUFFERED=1

# Copy dependency list into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into the container
COPY . .

# Make port 8000 available
EXPOSE 8000

# Start the MediBot FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
