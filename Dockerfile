FROM python:3.7-slim-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # graphviz dependencies
  && apt-get install -y python-pydot python-pydot-ng graphviz \
  && apt-get install -y libmagic-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


RUN mkdir /code
# COPY ./entrypoint /code/entrypoint
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

RUN pwd
# windows <-> linux
RUN sed -i 's/\r$//g' ./entrypoint
RUN chmod +x ./entrypoint

ENTRYPOINT ["./entrypoint"]