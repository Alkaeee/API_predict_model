FROM python:3.11.5

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app_v0.py"]

ENV FLASK_APP=app

EXPOSE 5000