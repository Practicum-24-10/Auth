# Auth
## Сервис аутентификации и авторизации


### Запуск приложения в контейнере
- Создать файл .env по примеру .env.example и выполнить команду:
```
docker compose up
```

### Запуск тестов в контейнере
- Создать файл .env по примеру .env.example и tests/.env по примеру tests/.env.example, выполнить команду:
```
docker compose -f tests/functional/docker-compose.yml up
```

### Запуск приложения локально

- Запустить и активировать виртуальное окружение, установить пакеты из requirements.txt:
```
python3.10 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

- Создать файл .env по примеру .env.dev.example

- Поднять PostgreSql и Redis:
```
docker compose -f docker-compose.dev.yml up
```

- Выполнить миграции:
```
flask --app src/app db upgrade --directory src/migrations
```

- Запустить Flask:
```
flask --app src/app run
```

- Создать суперпользователя:
```
flask --app src/app create superuser
```

### Запуск тестов локально
- Запустить приложение локально
- Создать файл tests/.env по примеру tests/.env.example и выполнить команду:
```
pytest tests/functional/src_tests
```

### Swagger
- [http://localhost/docs/](http://localhost/docs/)


### Схемма данных
![Схемма данных](https://raw.githubusercontent.com/Practicum-24-10/Auth/main/data_schema.jpeg?token=GHSAT0AAAAAACB6H32D57FGEXC3VE2TO62GZDY6M6A)