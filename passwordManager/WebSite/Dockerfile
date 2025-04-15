# syntax=docker/dockerfile:1
FROM alpine:3.14

ENV PYTHONUNBUFFERED=1
RUN adduser -Ds /bin/sh -u 1000 app
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install --no-cache Flask pymongo==4.12 gunicorn==22.0.0 cryptography==39.0.1
RUN mkdir /home/app/static/ /home/app/templates/

COPY ["*.py", "/home/app/"]
COPY ["./templates/", "/home/app/templates/"]
COPY ["./static/", "/home/app/static/"]
WORKDIR "/home/app"
RUN chown -R app:app /home/app/
USER app

ENV FLASK_APP=app
EXPOSE 8000/tcp
CMD ["gunicorn", "--certfile=/run/secrets/cert", "--keyfile=/run/secrets/key", "-w", "4" ,"-b", "0.0.0.0:8000", "app:app"]
