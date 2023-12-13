FROM python:3.11.5-alpine AS builder

WORKDIR /src
COPY . /src
RUN apk add --no-cache build-base python3-dev libffi-dev \
    && pip install --upgrade pip \
    && pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "app_v0.py"]

FROM builder as dev-envs

EXPOSE 5000