# Base image is python
FROM python:3.13-slim

# Set working directory
WORKDIR /code

# Copy requirements
COPY ./requirements.txt /code/requirements.txt

# Install postgresql
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && apt-get clean \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy app inside container
COPY ./app /code/app

# Set entry point
CMD ["fastapi", "run", "app/main.py", "--port", "80"]