# syntax=docker/dockerfile:1
FROM alpine:3.14

ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install --no-cache Flask pymongo gunicorn
RUN mkdir /home/static/ /home/templates/ /home/secrets/
WORKDIR "/home/"

COPY ["*.py", "./"]
COPY ["./templates/", "/home/templates/"]
COPY ["./static/", "/home/static/"]
COPY ./.nginx/rootCA.crt ./.nginx/rootCA.key /home/secrets/

ENV FLASK_APP=app
EXPOSE 8000/tcp
CMD ["gunicorn", "--certfile=/home/secrets/rootCA.crt", "--keyfile=/home/secrets/rootCA.key", "-w", "4" ,"-b", "0.0.0.0:8000", "app:app"]