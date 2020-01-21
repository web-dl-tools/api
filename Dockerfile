FROM python:3.8.1-buster

MAINTAINER rinesh.ramadhin@gmail.com

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["./service-check.sh", "./prepare.sh"]

CMD ["python manage.py runserver 0.0.0.0:8000"]
