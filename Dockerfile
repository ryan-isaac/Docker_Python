FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./

ADD weather_data.py /

RUN apt-get update

RUN pip3 install -r requirements.txt

RUN mkdir /output

COPY . .

CMD [ "python", "./weather_data.py" ]
