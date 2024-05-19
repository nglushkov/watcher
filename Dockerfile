FROM python:3.8

WORKDIR /var/www/app

COPY ./app/requirements.txt .

RUN pip install -r requirements.txt

CMD ["tail", "-f", "/dev/null"]
