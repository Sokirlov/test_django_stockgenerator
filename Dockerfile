FROM python:3.12-slim
LABEL authors="sokirlov"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
