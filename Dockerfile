# Use official Python image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1  
ENV PORT=5000  # Default PORT

# Set working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y python3-pip

# Copy everything
COPY . /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir tensorflow tf_keras numpy pandas tensorflow_hub flask flask_cors gunicorn

# Expose the port
EXPOSE 5000  

# Run Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
