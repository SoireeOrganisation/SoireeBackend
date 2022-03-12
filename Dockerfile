FROM python:3.9.5-slim-buster
WORKDIR /app

COPY app app
COPY requirements.txt main.py boot.sh ./
RUN python -m pip install --upgrade pip && pip3 install -r requirements.txt && chmod +x boot.sh \
&& apt-get update && apt-get install -y netcat

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]