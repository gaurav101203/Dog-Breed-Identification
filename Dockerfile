# Use an official Python image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy files to container
COPY . /app/

# Install dependencies
RUN python -m pip install --upgrade pip
RUN pip install tensorflow tf_keras numpy pandas tensorflow_hub flask flask_cors gunicorn

# Expose port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
