from django.http import JsonResponse
from django.db import connections
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Users, Stok, Oem
from .serializers import UserSerializer, StockSerializer, OemSerializer
import pymysql
from decouple import config
import time
from django.db.models import F

"""
    Функция для установления соединения с базой данных MySQL.
"""
def get_mysql_connection():
    return pymysql.connect(host=config('DATABASE_MYSQL_URL'),
                           user=config('DATABASE_MYSQL_USER'),
                           password=config('DATABASE_MYSQL_PASSWORD'),
                           database=config('DATABASE_MYSQL_DB'),
                           cursorclass=pymysql.cursors.DictCursor)

"""
    Получение всех записей о товарах из таблицы 'Stok'.

    Parameters:
        request (HttpRequest): Запрос от клиента.

    Returns:
        JsonResponse: JSON-ответ с данными о товарах и статусом HTTP.
"""
@api_view(['GET'])
def get_all_stock(request):
    if request.method == 'GET':
        stock = Stok.objects.all()
        serializer = StockSerializer(stock, many=True)
        return Response(serializer.data)

"""
    Получение всех записей о пользователях из таблицы 'Users'.

    Parameters:
        request (HttpRequest): Запрос от клиента.

    Returns:
        JsonResponse: JSON-ответ с данными о пользователях и статусом HTTP.

"""
@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

"""
    Получение всех записей о производителях OEM из таблицы 'Oem'.

    Parameters:
        request (HttpRequest): Запрос от клиента.

    Returns:
        JsonResponse: JSON-ответ с данными о производителях OEM и статусом HTTP.

"""
@api_view(['GET'])
def get_all_oem(request):
    if request.method == 'GET':
        oem = Oem.objects.all()
        serializer = OemSerializer(oem, many=True)
        return Response(serializer.data)

"""
    Получение всех заказов из таблицы 'shop_orders'.

    Parameters:
        request (HttpRequest): Запрос от клиента.

    Returns:
        JsonResponse: JSON-ответ с данными о заказах и статусом HTTP.

"""
@api_view(['GET'])
def get_shop_orders(request):
    if request.method == 'GET':
        connection = get_mysql_connection()
        
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM shop_orders")
                result = cursor.fetchall()
        
        return JsonResponse(result, safe=False)

"""
    Получение информации о товаре на основе артикула.

    Parameters:
        request (HttpRequest): Запрос от клиента.

    Returns:
        JsonResponse: JSON-ответ с информацией о товаре и статусом HTTP.

"""
@api_view(['POST'])
def get_article(request):
    try:
        data = request.data
        article = data.get('article')
        login = data.get('login')
        password = data.get('password')

        # Check user credentials
        user = Users.objects.filter(login=login).first()
        if not user:
            return JsonResponse(
                {'error': 'Пользователь не найден'}, 
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                status=404
            )
        if user.password != password:
            return JsonResponse(
                {'error': 'Неправильный пароль'}, 
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                status=401
            )
        
        user.ch = F('ch') + 1 
        user.save(update_fields=['ch']) 

        # Check article in 'oem' table
        article_record = Oem.objects.filter(oem=article).first()
        if article_record:
            # print('article_record:', article_record)
            # If found in 'oem' table, search in 'stok' table
            article_record2 = Stok.objects.filter(article=article_record.art).first()
            if article_record2:
                # print('article_record2:', article_record)
                clean_price = article_record2.price.replace(',', '.').strip()
                discount_amount = (float(clean_price) * user.dis) / 100
                discounted_price = "{:.2f}".format(float(clean_price) - discount_amount)

                article_data = {
                    'article': article_record2.article.strip(),
                    'name': article_record2.nam.strip(),
                    'oem': article_record2.oem.strip(),
                    'price': discounted_price,
                    'quantity': article_record2.quantity.strip(),
                    'brand': article_record2.brand.strip(),
                }
                # return JsonResponse(article_data)
                return JsonResponse(
                {'message': 'Информация по товару', 'article_data': article_data},
                safe=False,
                json_dumps_params={'ensure_ascii': True},
                status=200
            )
            else:
                return JsonResponse(
                    {'error': 'Артикул не найден'}, 
                    safe=False,
                    json_dumps_params={'ensure_ascii': True},  
                    status=404
                )
        else:
            return JsonResponse(
                {'error': 'Артикул не найден'},
                safe=False,
                json_dumps_params={'ensure_ascii': True},  
                status=404
            )

    except Exception as e:
        print('Произошла ошибка:', e)
        return JsonResponse(
            {'error': 'Произошла ошибка'}, 
            safe=False,
            json_dumps_params={'ensure_ascii': True}, 
            status=500
        )

"""
    Создание нового заказа.

    Parameters:
        request (HttpRequest): Запрос от клиента.

    Returns:
        JsonResponse: JSON-ответ с результатом создания заказа и статусом HTTP.

"""
@api_view(["POST"])
def create_order(request):
    # Получение данных из запроса
    data = request.data
    login = data.get('login')
    password = data.get('password')
    order_items = data.get('order')
    # print('login: ', login)
    # print('password: ', password)

    # Проверка учетных данных пользователя
    if not Users.objects.filter(login=login).exists():
        return JsonResponse(
            {'error': 'Пользователь не найден'}, 
            safe=False,
            json_dumps_params={'ensure_ascii': True},  
            status=404
        )

    user = Users.objects.get(login=login)
    if user.password != password:
        return JsonResponse(
            {'error': 'Неправильный пароль'},
            safe=False,
            json_dumps_params={'ensure_ascii': True}, 
            status=401
        )
    
    user.ch = F('ch') + 1 
    user.save(update_fields=['ch']) 

    # Подключение к MySQL базе данных используя pymysql
    mysql_conn = get_mysql_connection()

    try:
        with mysql_conn.cursor() as cursor:
            # Добавление нового заказа в `shop_orders` и получение его ID
            cursor.execute("""INSERT INTO shop_orders (user_id, time, successfully_created, status, paid, paid_time, 
            how_get, how_get_json, office_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (user.id , int(time.time()), 1, 1, 0, 0, 1, '{"mode":1,"office_id":2}', 2))
            order_id = cursor.lastrowid
            
            # Для каждого заказа, добавляем записи в `shop_order_items`
            for item in order_items:
                article = item['article']
                # print('article: ', article)
                quantity = item['quantity']
                # print('quantity: ', quantity)

                if not Stok.objects.filter(article=article).exists():
                    return JsonResponse(
                        {'error': f'Артикул {article} не найден'}, 
                        safe=False,
                        json_dumps_params={'ensure_ascii': True}, 
                        status=404
                    )
                
                # Получаем информацию из таблицы Stok из MSSQL базы данных
                stok_item = Stok.objects.get(article=article)

                # Очищаем цену, если вместо точки используется запятая для разделения значений после запятой
                clean_price = stok_item.price.replace(',', '.').strip()
                clean_quantity = int(quantity)

                discount_amount = (float(clean_price) * user.dis) / 100
                discounted_price = float(clean_price) - discount_amount

                cursor.execute("""INSERT INTO shop_orders_items (order_id, product_type, price, count_need, product_id,
                t2_manufacturer, t2_article, t2_article_show, t2_name, t2_exist, t2_time_to_exe, t2_time_to_exe_guaranteed, t2_min_order, t2_probability, t2_markup, t2_price_purchase, 
                t2_office_id, t2_storage_id, sao_state, sao_robot, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (order_id, 2, clean_price, clean_quantity, 0, stok_item.brand, article.replace('-', ''), article, stok_item.nam, 
                1, 0, 0, 0, 100, -user.dis, discounted_price, 2, 57, 0, 0, 1))

            mysql_conn.commit()
    except pymysql.MySQLError as e:
        # При неудачной обработке отменяем запросы к базе и возвращаем ошибку
        mysql_conn.rollback()
        return JsonResponse(
            {'error': f'Ошибка базы данных: {str(e)}'}, 
            safe=False,
            json_dumps_params={'ensure_ascii': True}, 
            status=500
        )
    finally:
        mysql_conn.close()

    return JsonResponse(
        {'message': 'Заказ создан успешно', 'order_id': order_id},
        safe=False,
        json_dumps_params={'ensure_ascii': True},
        status=201
    )

@api_view(["POST"])
def get_order_details(request):
    # Подключение к MySQL базе данных используя pymysql
    mysql_conn = get_mysql_connection()

    # Получение данных из запроса
    data = request.data
    login = data.get('login')
    password = data.get('password')
    order_id = data.get('order_id')
    # print('login: ', login)
    # print('password: ', password)
    # print('order_id: ', order_id)

# Проверка учетных данных пользователя
    if not Users.objects.filter(login=login).exists():
        return JsonResponse(
            {'error': 'Пользователь не найден'},
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            status=404
        )

    user = Users.objects.get(login=login)
    if user.password != password:
        return JsonResponse(
            {'error': 'Неправильный пароль'},
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            status=401
        )
    
    user.ch = F('ch') + 1 
    user.save(update_fields=['ch']) 

    try:
        with mysql_conn.cursor() as cursor:
            # Проверяем наличие заказа и его принадлежность к логину
            cursor.execute("SELECT id FROM shop_orders WHERE id = %s AND user_id = %s", (order_id, user.id))
            order = cursor.fetchone()
            if not order:
                return JsonResponse(
                    {'error': 'Заказ не найден или доступ запрещен'},
                    safe=False,
                    json_dumps_params={'ensure_ascii': True},
                    status=404
                )

            # Получение деталей заказа
            cursor.execute("""SELECT count_need, status, t2_manufacturer, t2_article_show, t2_name
                              FROM shop_orders_items WHERE order_id = %s""", (order_id,))
            order_items = cursor.fetchall()
            if not order_items:
                return JsonResponse(
                    {'error': 'Детали заказа не найдены'},
                    safe=False,
                    json_dumps_params={'ensure_ascii': True},
                    status=404)
    except pymysql.MySQLError as e:
        # При неудачной обработке отменяем запросы к базе и возвращаем ошибку
        mysql_conn.close()
        return JsonResponse(
            {'error': f'Ошибка базы данных: {str(e)}'},
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            status=500
        )
    else:
        mysql_conn.close()
        return JsonResponse(
            {'message': 'Данные заказа', 'order_id': order_id, 'order_items': order_items},
            safe=False,
            json_dumps_params={'ensure_ascii': True},
            status=200
        )

@api_view(["GET"])
def test_endpoint(request):
    # Возвращаем ответ с сообщением о том, что сервер работает
    return JsonResponse(
        {'message': 'Сервер работает'},
        safe=False,
        json_dumps_params={'ensure_ascii': True},
        status=200 
    )