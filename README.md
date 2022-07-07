# Тестовое задание для Joom: бэкенд сервиса календаря

**Стек**: Python3, FastAPI, PostgreSQL, Docker, Docker Compose

### Инструкция для запуска

Для запуска задания нужно сделать следующее:

``` 
git clone https://github.com/deltamachine/joom_calendar_service.git

cd joom_calendar_service

docker-compose up --build -d
```

Это запустит приложение по адресу http://0.0.0.0:8004/.

Описание API-эндпойнтов (Swagger) можно найти по адресу http://0.0.0.0:8004/docs

Тесты можно запустить командой ```docker exec web pytest core/tests/```

### Техническое задание

Сервис должен иметь HTTP API, позволяющее:
- [x] создать пользователя
- [x] создать встречу в календаре пользователя со списком приглашенных пользователей
- [x] получить детали встречи
- [x] принять или отклонить приглашение другого пользователя
- [x] найти все встречи пользователя для заданного промежутка времени
- [x] для заданного списка пользователей и минимальной продолжительности встречи, найти ближайшей интервал времени, в котором все эти пользователи свободны
- [x] У встреч в календаре должна быть возможна настройка повторов. В повторах нужно поддержать все возможности, доступные в Google-календаре, кроме Сustom.

**Необязательные требования:**
 - [x] аутентификация пользователя
 - [x] поддержка видимости встреч (если встреча приватная, другие пользователи могут получить только информацию о занятости пользователя, но не детали встречи)
 - [ ] настройки часового пояса пользователя и его рабочего времени, использование этих настроек для поиска интервала времени, в котором участники свободны
 - [ ] настройки нотификации пользователя перед встречей (саму нотификацию достаточно реализовать записью в лог)
 - [x] поддержка Custom повторов, как в Google-календаре
