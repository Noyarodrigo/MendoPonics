
#base image
FROM python:3.8-slim

RUN apt-get update -y && apt-get upgrade python3-pip -y
RUN python3 -m pip install --upgrade pip
RUN pip3 install --upgrade setuptools

WORKDIR /app/src

COPY ./ ./

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python", "emailSender.py"]
