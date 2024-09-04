# stage 1: pull a base python image
FROM python:3.12-slim as python

# stage 2: set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# stage 3: set work directory
WORKDIR /app

# stage 4: install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --cache-dir .pip-cache -r requirements.txt && \
    rm -rf .pip-cache

# stage 5: copy project
COPY . .

# stage 6: run
# Expose the port the app runs on
# EXPOSE 8000

# Copy Gunicorn configuration
COPY gunicorn_config.py /app/gunicorn_config.py

# Run Gunicorn with the specified configuration file
CMD ["gunicorn", "-c", "gunicorn_config.py", "config.wsgi:application"]