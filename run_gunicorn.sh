#!/usr/bin/env bash

flask --app src/app db upgrade --directory src/migrations

gunicorn src.app:app --bind 0.0.0.0:8000
