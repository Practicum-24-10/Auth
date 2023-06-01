FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PYTHONPATH=/app/

COPY run_gunicorn.sh run_gunicorn.sh
RUN chmod +x  /app/run_gunicorn.sh
COPY requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["/app/run_gunicorn.sh"]
