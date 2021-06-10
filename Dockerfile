FROM python:3.9

USER root

RUN apt-get update -y
RUN apt-get install -y g++ libsasl2-dev libsasl2-modules

WORKDIR /code

COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY ./ ./

EXPOSE 8051

CMD ["python", "./index.py"]