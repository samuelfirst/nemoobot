#pull official base image
# TODO use alpine image
FROM python:3.9.0

#set enviroment variables
ENV PYTHONFONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .