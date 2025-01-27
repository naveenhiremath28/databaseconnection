FROM python:3.12-slim

WORKDIR /app

RUN pip install fastapi[all] uvicorn sqlalchemy

COPY . /app/

EXPOSE 8000

CMD ["python3", "app/main.py"]

