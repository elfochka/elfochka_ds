FROM python:3.11.1-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#COPY . .
COPY clickomarket /app/clickomarket
COPY keys.py /app/

# Сначала запускаем файл, в котором будут записаны ключи в .env
CMD ["/bin/bash", "-c", "python3 keys.py && sleep 1 && python manage.py runserver 0.0.0.0:8000"]


