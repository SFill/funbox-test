Links: тестовое на python 3.7 для funbox.ru
==============================

Установка
---------------

Поднять redis
```sh
$ docker run -p 127.0.0.1:6379:6379 --name redis-instance -d redis
```

Создать виртуальное окружение и активировать его
```sh
$ python3 -m venv venv
$ source  venv/bin/activate
```

Установка пакета
```sh
$ pip install -e .
```


Запуск
-------
```sh
$ export FLASK_APP=links.app
$ flask run
```
Запуститься на  http://127.0.0.1:5000

Тесты
-------
```sh
$ pip install '.[test]'
$ pytest
```