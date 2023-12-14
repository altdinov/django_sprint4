# Описание
Платформа для публикации постов. Можно создавать собсвенные посты и читать посты других пользователей.

# Стек:
Python, Django

# Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:altdinov/django_sprint4.git
```

```
cd django_sprint4
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
