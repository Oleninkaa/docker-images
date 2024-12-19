FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip


RUN pip install -r requirements.txt



COPY . .

RUN chmod +x /app/django.sh

RUN mkdir -p /app/media

EXPOSE 8000

ENTRYPOINT [ "/app/django.sh" ]
