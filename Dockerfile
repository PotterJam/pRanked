FROM node:18-alpine AS frontend-stage

WORKDIR /frontend
COPY frontend/package*.json .
RUN npm ci
COPY frontend /frontend/

ENV PUBLIC_BASE_URL='https://p-ranked.fly.dev/api'

RUN npm run build
RUN npm prune --production

FROM python:3.12 as requirements-stage

WORKDIR /tmp
RUN pip install poetry
COPY backend/pyproject.toml backend/poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.12

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY backend /code/app/
COPY --from=frontend-stage /frontend/build /code/frontend/dist/

ENV PYTHONPATH "/code/app/"


ADD https://github.com/benbjohnson/litestream/releases/download/v0.3.9/litestream-v0.3.9-linux-amd64-static.tar.gz /tmp/litestream.tar.gz
RUN tar -C /usr/local/bin -xzf /tmp/litestream.tar.gz

COPY ./litestream.yml /etc/litestream.yml

ENV DB_PATH '/code/app/db.sqlite'
ENV LITESTREAM_ACCESS_KEY_ID ''
ENV LITESTREAM_SECRET_ACCESS_KEY ''

ENV ADMIN_PASSWORD ''
ENV AUTH_COOKIE_VALUE ''

EXPOSE 8080

CMD \
 # if the db file doesn't exist we get it from the REPLICA_URL $DB_PATH "${REPLICA_URL}" | $DB_PATH $REPLICA_URL
 [ ! -f $DB_PATH ] && litestream restore -if-replica-exists $DB_PATH \
 ; litestream replicate -exec "uvicorn app.main:app --host 0.0.0.0 --port 8080"