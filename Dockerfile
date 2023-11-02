# ---------- Requirements ----------
FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# ---------- Release ----------
FROM python:3.11-slim

# keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /code

# install dependencies
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# copy project
COPY ./app /code/app

# copy logging config
COPY ./logging.conf /code/logging.conf

# CMD ["python", "app/main.py", "liv2023_min.xlsx"]