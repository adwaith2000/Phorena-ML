FROM ubuntu:latest
ENV LANG C.UTF-8
RUN apt-get update && apt-get install -y software-properties-common && apt-add-repository universe
RUN apt-get update && apt-get install -y python python3.5 python3-pip
RUN pip3 install setuptools pip --upgrade --force-reinstall
COPY . /code/sensor
WORKDIR /code/sensor
RUN pip install -r requirements.txt
ENTRYPOINT ["python3", "-u", "sensor.py"]