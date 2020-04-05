# pull official base image
FROM nikolaik/python-nodejs:python3.8-nodejs12

# set work directory
WORKDIR /usr/local/site/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PG_VERSION=11

# install psycopg2 dependencies
RUN set -ex \
    && apt-get update \
    && apt-get install  -y\
       gcc \
       g++ \
       postgresql-server-dev-$PG_VERSION \
       musl-dev \
    && apt-get install -y \
       gettext \
       postgresql-client-$PG_VERSION \
    && apt-get install  -y\
       binutils libproj-dev libgeos++ proj-bin libgdal20 python3-gdal

# install dependencies
RUN set -ex && \
    pip install --upgrade pip
COPY ./backend/requirements.txt /usr/local/site/requirements.txt
RUN set -ex && \
    pip install -r requirements.txt

# copy project
COPY ./backend /usr/local/site/

# Node setup
RUN npm ci --no-optional
ENV PATH $PATH:/usr/local/site/node_modules/.bin:$PATH

CMD ["forever", "start", "./server.js", "&&", "python", "manage.py", "runserver", "0.0.0.0:8008",]