FROM python:3.10-slim-bullseye

WORKDIR /TwitterFlightBot

ADD requirements.txt .
RUN apt update && apt install -y build-essential
RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

ADD *.py ./
ADD ./logs ./logs

ENTRYPOINT ["python", "main.py"]
