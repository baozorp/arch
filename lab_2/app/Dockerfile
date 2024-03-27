FROM python:3.12
WORKDIR /messenger_app

COPY ./requirements.txt /messenger_app/requirements.txt
RUN pip install -r requirements.txt

COPY . /messenger_app

ENTRYPOINT ["bash", "-c", "cd ./rest-api && uvicorn main:app --port 8080 --host 0.0.0.0"]