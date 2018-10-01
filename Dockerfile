FROM alpine:3.8
LABEL maintainer="VirtualTam"

RUN apk --update --no-cache add \
        ca-certificates \
        gcc \
        musl-dev \
        python3 \
        python3-dev

ADD . /app
WORKDIR /app
RUN python3 setup.py install

RUN adduser -D -h /var/lib/botibal botibal
USER botibal
WORKDIR /var/lib/botibal
ADD config.example.ini config.ini

VOLUME /var/lib/botibal

CMD ["botibal", "-m", "config.ini", "db.sqlite3"]
