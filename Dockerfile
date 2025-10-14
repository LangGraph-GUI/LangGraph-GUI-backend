FROM python:3.12-slim

# Install necessary packages
RUN apt-get update && apt-get install -y cron supervisor

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy files to the /app directory
COPY ./src/ ./src/

# Ensure the workspace directory exists
RUN mkdir -p /app/src/workspace && mkdir -p /app/src/log

# for cron daily task
COPY daily.sh daily.sh
RUN chmod +x /app/daily.sh

# Copy cron configuration
COPY crontab /mycron
RUN chmod 644 /mycron
RUN crontab /mycron

# Copy Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Start Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
