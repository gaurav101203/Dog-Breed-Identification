# Use official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy everything
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir tensorflow tf_keras numpy pandas tensorflow_hub flask flask_cors gunicorn

# Expose the port (optional, but good practice)
EXPOSE 5000  

# Run the app
CMD ["gunicorn", "-w", "2", "app:app"]
