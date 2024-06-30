FROM python:3.12

ENV PYTHONUNBUFFERED = 1
ENV APP_DIR=/app

WORKDIR $APP_DIR/

ADD requirements.txt $APP_DIR

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
ADD . $APP_DIR

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --no-input

CMD python manage.py runserver 0.0.0.0:8000
