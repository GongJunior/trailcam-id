FROM python:3.8.18-bullseye

RUN apt-get update && apt install -y python3-opencv
WORKDIR /app
COPY src/requirements.txt .
RUN pip install -r requirements.txt
COPY src/ .

ENTRYPOINT [ "tail", "-f", "/dev/null" ]