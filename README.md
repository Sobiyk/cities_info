# cities_info


### Шаблон заполнения .env:

```
APP_NAME='string'
APP_VERSION='1.0.0'
DATABASE_URL='postgresql+asyncpg://postgres:postgres@localhost:1234/db_name'
GEO_API_URL='http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={token}'
GEO_API_TOKEN='token'
```

### Запустить сборку контейнеров
```
docker-compose up -d --build
```

### Применить миграции
```
docker exec -it cities_info-web-1 bash
alembic upgrade head
```

### Перейти в документацию
```
http://localhost:8000/docs
```