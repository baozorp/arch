FROM python:3.12
WORKDIR /init

COPY ./requirements.txt /init/requirements.txt
RUN pip install faker psycopg2-binary pymongo

COPY . /init

ENTRYPOINT ["bash", "-c", "python3 upload_script.py"]