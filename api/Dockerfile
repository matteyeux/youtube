FROM python:3.5-alpine
WORKDIR /api/
COPY ./src/requirements.txt .
RUN pip install -r requirements.txt
CMD ["python", "youtube.py"]