FROM python:3.12 as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.12

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app/

ENV PYTHONPATH "/code/app/"

ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.9/litestream-v0.3.9-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz
ENV DB_PATH '/code/app/db.sqlite'

COPY ./litestream.yml /etc/litestream.yml

# Make these available somehow at build time
#ENV LITESTREAM_ACCESS_KEY_ID ''
#ENV LITESTREAM_SECRET_ACCESS_KEY ''

EXPOSE 8080

CMD \
  # if the db file doesn't exist we get it from the REPLICA_URL $DB_PATH "${REPLICA_URL}" | $DB_PATH $REPLICA_URL
  [ ! -f $DB_PATH ] && litestream restore -if-replica-exists $DB_PATH \
  ; litestream replicate -exec "uvicorn app.main:app --host 0.0.0.0 --port 8080"