#e the official Python image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Install the dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the source code
COPY . .

# Set the command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

