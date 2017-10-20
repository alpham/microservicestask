FROM ubuntu:16.04

RUN set -x; \
            apt-get update \
            && apt-get install -y --no-install-recommends\
                 python3-pip \
                 python3-setuptools \
                 python3-uwsgidecorators \
                 build-essential \
                 python3-dev

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 80

CMD ["uwsgi", "--ini", "uwsgi.ini"]