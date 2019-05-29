########################
# Dockerfile for the 
# encoder microservice
########################
FROM python:3.5-alpine
WORKDIR /encoder
ADD src/ .
RUN  ls
RUN pip install -r requirements.txt
RUN apk update && apk add ffmpeg
