FROM python:3.11-slim

# Create a non-root user and group
RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser && \
    mkdir -p /home/src &&  \
    mkdir -p /home/config

# Grant the non-root user access to the application directories
RUN chown -R appuser:appgroup /home/src && \
    chown -R appuser:appgroup /home/config

ADD ./etc/ /home/config/
COPY requirements.txt /home/config/
WORKDIR /home/src

# Install required packages and Python dependencies
RUN apt-get update && \
    apt-get install -y gcc && \
    pip install --no-cache-dir -r /home/config/requirements.txt

# Switch to the non-root user
USER appuser

CMD [ "uwsgi", "--ini", "/home/config/uwsgi.ini", "--http", "0.0.0.0:80" ]
#CMD [ "sh", "-c", "python webhook.py & rq worker --url 'redis://redis' bot" ]
