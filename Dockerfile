FROM python:3.12-alpine

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps \
        gcc \
        musl-dev \
        libxml2-dev \
        libxslt-dev \
        libffi-dev \
    && apk add --no-cache \
        libxml2 \
        libxslt \
        libffi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps \
    && rm -rf /var/cache/apk/* /root/.cache /tmp/*

COPY server.py app.py ./
COPY endpoints ./endpoints/

EXPOSE 1235

CMD ["python", "app.py"]
