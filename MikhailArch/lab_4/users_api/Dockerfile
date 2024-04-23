FROM python:3.12
WORKDIR /messenger_app

RUN pip install psycopg2-binary "fastapi[all]" pyjwt

COPY . /messenger_app

ENTRYPOINT ["bash", "-c", "cd ./rest-api && uvicorn main:app --port 8080 --host 0.0.0.0"]