FROM python:3

RUN mkdir -p /app
WORKDIR /app

COPY freeposte ./freeposte
COPY manage.py .
COPY requirements.txt .
COPY start.sh /start.sh

RUN pip install -r requirements.txt

CMD ["/start.sh"]
