FROM python:3.12
WORKDIR /app

RUN pip install Faker && pip install motor

COPY . /app

ENTRYPOINT ["bash", "-c", "python3 init_data.py"]