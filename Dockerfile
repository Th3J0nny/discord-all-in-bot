# syntax=docker/dockerfile:1
FROM python:3.9

WORKDIR ~/discord-all-in-bot

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./main.py"]
