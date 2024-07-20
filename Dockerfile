# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.10

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . .
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip || true
RUN pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install

EXPOSE 8000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
CMD ["run"]

