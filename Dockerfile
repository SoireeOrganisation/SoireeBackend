FROM tiangolo/uwsgi-nginx-flask:python3.10

COPY app app/
COPY main.py requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

ENV FLASK_APP app.py