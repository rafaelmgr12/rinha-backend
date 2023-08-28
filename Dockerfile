# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster AS base

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory in the container
WORKDIR /app

# Copy project requirement files
COPY ./requirements.txt ./
COPY .env ./

# Install any needed packages and Python dependencies
RUN apt-get update && apt-get -y install libpq-dev gcc \
    && pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the working directory contents into the container
COPY ./src /app/src
COPY main.py /app/


# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run app when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]