# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.10

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app
COPY . /app
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - && poetry --version
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod -R 777 app_data

EXPOSE 8000

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
CMD ["run"]

