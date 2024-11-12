FROM python:latest

WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the app's code
COPY . .

# Expose the port that Flask runs on
EXPOSE 5000

# Start the Flask application
CMD ["python", "run.py"]
