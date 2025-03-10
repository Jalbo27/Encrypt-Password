# syntax=docker/dockerfile:1
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install Flask pymongo
RUN mkdir /home/static/ /home/templates/
WORKDIR "/home/"

COPY ["*.py", "./"]
COPY ["./templates/", "/home/templates/"]
COPY ["./static/", "/home/static/"]

ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000/tcp
CMD ["flask", "run", "--debug"]