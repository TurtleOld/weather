#!/bin/bash

run() {
  poetry run python ./manage.py migrate --noinput

  DJANGO_SUPERUSER_USERNAME="$SUPERUSER_USERNAME" \
  DJANGO_SUPERUSER_PASSWORD="$SUPERUSER_PASSWORD" \
  DJANGO_SUPERUSER_EMAIL="$SUPERUSER_EMAIL" \
  poetry run python ./manage.py createsuperuser --noinput

  poetry run python ./manage.py runserver --noreload 0.0.0.0:8000
}

if [ "$#" -gt 0 ]; then
  case $1 in
    run)
      run && exit 0 || exit 1
      ;;
    sh)
      sh
      exit 0
      ;;
    *)
      run && exit 0 || exit 1
      ;;
  esac
fi

run
