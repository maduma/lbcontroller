FROM python:3.8.2-slim

COPY . src
RUN cd src && pip install -r requirements.txt && pip install .
