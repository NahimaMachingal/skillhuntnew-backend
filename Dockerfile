#backend Dockerfile

FROM python:3.10-alpine

# Install dependencies for psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app/

# Set the working directory
WORKDIR /app

# In your Dockerfile
RUN mkdir -p /app/media

# Expose the port the app runs on
EXPOSE 8000

# Start the application with Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]

