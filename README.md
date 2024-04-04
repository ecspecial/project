# stock-api

# Оглавление

1. [Предварительные требования](#предварительные-требования)
2. [Начало работы](#начало-работы)
    - [Копирование проекта с GitHub](#копирование-проекта-с-github)
    - [Настройка файла .env](#настройка-файла-env)
    - [Установка зависимостей](#установка-зависимостей)
    - [Запуск программы](#запуск-программы)
3. [Описание методов POST](#описание-методов-post)
4. [Синхронизация репозитория](#синхронизация-репозитория)

## Предварительные требования

Для работы с проектом вам потребуется:

- Python 3.6 или выше
- MS SQL Server
- (Опционально) SQL Server Management Studio (SSMS) для управления базой данных
- MySQL дистанционный сервер

## Начало работы

Для начала работы с проектом выполните следующие шаги.

### Копирование проекта с GitHub

1. Убедитесь в том, что Python установлен с помощью команды ```python --version```
2. Склонируйте репозиторий на локальную машину с помощью команды: ```git clone https://github.com/ecspecial/project.git```
3. Перейдите в директорию проекта: ```cd project```

### Настройка файла .env
1. Добавьте в файл `.env` строки со значениями переменных окружения для подключения к базе данных

### Установка зависимостей

1. Создайте виртуальное окружение и активируйте его:

- Для Windows:

  ```
  python -m venv venv
  .\venv\Scripts\activate
  ```

- Для macOS и Linux:

  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

2. Установите необходимые пакеты из файла `requirements.txt` с помощью команды: ```pip install -r requirements.txt```

### Запуск программы

Запустите приложение с помощью команды: ```python manage.py runserver```


## Описание методов POST

### Метод `POST /get_article` предназначен для получения информации о товаре по его артикулу. Для использования метода необходимо отправить JSON-запрос со следующей структурой:

Тестирование можно проводить при помощи Postman, отправляя запросы на адрес http://localhost:5000/get_article

```json
{
  "article": "oem_товара",
  "login": "ваш_логин",
  "password": "ваш_пароль"
}

Если указанный логин и пароль верны, и товар с указанным артикулом существует в базе данных, метод вернет JSON-ответ с информацией о товаре:
{
    "message": "Информация по товарам",
    "article_data_list": [
        {
            "article": "JPCP507-640",
            "name": "FOCUS 14- CT4Z16003A (ФРОНТОВОЕ СТЕКЛО)",
            "oem": "68051223AB",
            "price": "733.01",
            "quantity": "1",
            "brand": "BodyParts"
        },
        {
            "article": "FDFOC14-020-R",
            "name": "FOCUS 14- CT4Z16003A (ФРОНТОВОЕ СТЕКЛО)",
            "oem": "1866225",
            "price": "1858.95",
            "quantity": "5",
            "brand": "BodyParts"
        },
        {
            "article": "RNLOG05-331",
            "name": "2",
            "oem": "1866225",
            "price": "0.90",
            "quantity": "1",
            "brand": "BodyParts"
        },
        {
            "article": "RNLOG05-331",
            "name": "2",
            "oem": "1866225",
            "price": "0.90",
            "quantity": "1",
            "brand": "BodyParts"
        },
        {
            "article": "LDLAR12-330",
            "name": "4",
            "oem": "4",
            "price": "3.60",
            "quantity": "4",
            "brand": "4"
        }
    ]
}

В случае ошибки (например, неверный логин/пароль или товар не найден) метод вернет соответствующее сообщение об ошибке.
```
### Создание нового заказа

Метод POST, который создает новый заказ в системе.

### URL http://127.0.0.1:8000/api/create-order/

### Тело запроса (Пример)

```json
{
    "login": "user1",
    "password": "password",
    "order": [
        {
            "article": "JPCP507-640",
            "quantity": 2
        }
    ]
}

Ответ:
{
    "message": "Заказ создан успешно",
    "order_id": 12467
}
```

### Получение деталей заказа
Метод POST, который возвращает детали заказа по его ID.

### URL http://127.0.0.1:8000/api/order-details/

Тело запроса (Пример)
```json
{
    "login": "user1",
    "password": "password",
    "order_id": "12467"
}

Ответ
{
    "message": "Данные заказа",
    "order_id": "12467",
    "order_items": [
        {
            "count_need": 2,
            "status": 1,
            "name_status": "Отказ клиента",
            "t2_manufacturer": "BodyParts",
            "t2_article_show": "JPCP507-640",
            "t2_name": "FOCUS 14- CT4Z16003A (ФРОНТОВОЕ СТЕКЛО)"
        }
    ]
}
```

### Создание нового пользователя

Метод POST, который создает нового пользователя в системе. Обязательно прописать в .env параметры `MASTER_LOGIN=login` и `MASTER_PASSWORD=password` с желаемыми данными для авторизации.

### URL http://127.0.0.1:8000/api/add-user/

### Тело запроса (Пример)
```json
{
    "master_login": "login",
    "master_password": "password",
    "new_user": {
        "login": "user0",
        "password": "password",
        "dis": 10
    }
}

Ответ
{
    "message": "Пользователь добавлен успешно",
    "user": {
        "id": 4,
        "login": "user0",
        "dis": 10,
        "ch": 0
    }
}
```

### Получение всех товаров со скидкой клиента

Метод POST, который позволяет получить все товары со скидкой клиента

### URL http://127.0.0.1:8000/api/get-all-stock/

### Тело запроса (Пример)
```json

{
    "login": "user0",
    "password": "password"
}


Ответ

{
    "message": "Данные по товарам",
    "cards": [
        {
            "product_article": "JPCP507-640",
            "product_nam": "FOCUS 14- CT4Z16003A (ФРОНТОВОЕ СТЕКЛО)",
            "product_oem": "68051223AB",
            "product_new_item": null,
            "product_brand": "BodyParts",
            "product_price": "13240"
        },
        {
            "product_article": "RNLOG05-331",
            "product_nam": "FOCUS 14- CT4Z16003A (ФРОНТОВОЕ СТЕКЛО)",
            "product_oem": "68051223AB",
            "product_new_item": null,
            "product_brand": "BodyParts",
            "product_price": "13900"
        },
        {
            "product_article": "LDLAR12-330",
            "product_nam": "FOCUS 14- CT4Z16003A (ФРОНТОВОЕ СТЕКЛО)",
            "product_oem": "68051223AC",
            "product_new_item": null,
            "product_brand": "BodyParts",
            "product_price": "46462"
        },
    ]
}

```

### Получение всех статусов товаров

Метод Get, который позволяет получить все статусы товара

### URL http://127.0.0.1:8000/api/get-all-item-statuses/

### Пример ответа
```json

Ответ

{
    "message": "Данные по статусам",
    "statuses": [
        {
            "id": 1,
            "name": "Ожидает оплаты",
            "color": "#E7FF87",
            "for_created": 1,
            "order": 6,
            "count_flag": 1,
            "issue_flag": 0
        },
        {
            "id": 5,
            "name": "Выдан",
            "color": "#FFFFE1",
            "for_created": 0,
            "order": 1,
            "count_flag": 1,
            "issue_flag": 1
        }
    ]
}

```


## Синхронизация репозитория

Для синхронизации локального репозитория с обновленным репозиторием на GitHub выполните команду ```git pull``` и повторно выполните установку модулей ```pip install -r requirements.txt``` 