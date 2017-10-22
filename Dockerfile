FROM python:2.7-alpine
MAINTAINER coder4
RUN apk update && apk --no-cache add build-base
RUN apk --no-cache add openssl-dev libffi-dev
RUN pip install --no-cache-dir docker[tls] bottle cachetools 

# Dir
RUN mkdir -p /etc/dsd/machines /app
WORKDIR /app

# Expose
EXPOSE 8080

# File
COPY ./app.py ./config.py docker_query_service.py utils.py docker_client_helper.py /app/ 

# Run
CMD python ./app.py


