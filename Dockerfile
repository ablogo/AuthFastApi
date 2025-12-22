FROM python:3.13-slim

WORKDIR /app

COPY ./requirements.txt ./
COPY ./*.pem ./
COPY .env ./
COPY *.ini ./

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80", "--reload" ]