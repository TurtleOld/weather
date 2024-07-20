Установка и запуск приложения
-----------------------------
Запустить приложение вы можете через Poetry или Docker.

Установить **Poetry** командой:

**Linux**

.. code-block::

    sudo apt install python3-poetry -y

**macOS, Windows (WSL):**

.. code::

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

|

Подробная инструкция по установке **Poetry** доступна в [официальной документации](https://python-poetry.org/docs/).

Для установки **Poetry** и приложения, потребует версия **Python 3.9+** [Официальная документация на python.org](https://www.python.org/downloads/)

Для установки **Docker**, используйте информацию в официальной документации на [docs.docker.com](https://docs.docker.com/engine/install/)

----------

1. Установка
------------
1.1 Клонирование репозитория и активация виртуального окружения
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
|

Клонирование репозитория
########################
.. code::

    git clone https://github.com/TurtleOld/weather.git
    cd weather

|

Если используете **Poetry**
###########################

Активация виртуального окружения:

.. code::

    make shell

Если будет ошибка: Command 'make' not found...
Выполните в консоли команду

.. code::

    sudo apt install make

Затем:

.. code::

    make install

|

----------

1.2 Заполнение значений в .env файле
'''''''''''''''''''''''''''''''''''''

SECRET_KEY - Key for a file settings.py.
You can to generation the key on command - `make secretkey`

    SECRET_KEY=

DEBUG - Activation of debugging. Do not activate on a productive server.
Specify one of three values: true, 1, yes

    DEBUG=

    DJANGO_SUPERUSER_USERNAME - default admin
    DJANGO_SUPERUSER_PASSWORD - default admin
    DJANGO_SUPERUSER_EMAIL - default admin@admin.ru


-----------------

1.3 Завершение установки
''''''''''''''''''''''''
|

Если используете **Poetry**
###########################
.. code::

    make setup

|

2. Запуск приложения для разработки
'''''''''''''''''''''''''''''''''''
|

Если используете **Poetry**
###########################

.. code::

    make start


Если используете **Docker**
###########################
.. code::

    make up
