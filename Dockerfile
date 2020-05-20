FROM python:3.8

WORKDIR /app

RUN pip install poetry
COPY pyproject.toml /app/pyproject.toml
COPY poetry.lock /app/poetry.lock
RUN poetry config virtualenvs.create false
RUN poetry install -E uwsgi

ENTRYPOINT [ "uwsgi", "--py-autoreload", "1", "uwsgi.ini" ]