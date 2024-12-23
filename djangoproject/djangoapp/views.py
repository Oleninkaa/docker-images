import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_datetime
from django.http import JsonResponse, HttpResponse
from PIL import Image
import io

from django.core.serializers.json import DjangoJSONEncoder
import json

from .models import Customer, Ticket, Order, Seller
from .serializers import CustomerSerializer, TicketSerializer, OrderSerializer, SellerSerializer


#===== GETTING
# Отримати всіх продавців (MongoDB)
@api_view(['GET'])
def getSellers(request):
    sellers = Seller.objects.all()
    serializer = SellerSerializer(sellers, many=True)
    return Response(serializer.data)

# Отримати одного продавця (MongoDB)
@api_view(['GET'])
def getSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
        serializer = SellerSerializer(seller)
        return Response(serializer.data)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

# Отримати всіх клієнтів (PostgreSQL)
@api_view(['GET'])
def getCustomers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)

# Отримати одного клієнта (PostgreSQL)
@api_view(['GET'])
def getCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

# Отримати всі квитки (PostgreSQL)
@api_view(['GET'])
def getTickets(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data)

# Отримати один квиток (PostgreSQL)
@api_view(['GET'])
def getTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)
    except Ticket.DoesNotExist:
        return Response({"error": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

# # Отримати всі замовлення (PostgreSQL)
# @api_view(['GET'])
# def getOrders(request):
#     orders = Order.objects.all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

# # Отримати одне замовлення (PostgreSQL)
# @api_view(['GET'])
# def getOrder(request, pk):
#     try:
#         order = Order.objects.get(id=pk)
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)
#     except Order.DoesNotExist:
#         return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)




#===== ADDING
# Створити нового продавця (MongoDB)
@api_view(['POST'])
def addSeller(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Створити нового клієнта (PostgreSQL)
@api_view(['POST'])
def addCustomer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Створити новий квиток (PostgreSQL)
@api_view(['POST'])
def addTicket(request):
    serializer = TicketSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Створити нове замовлення (PostgreSQL)
# @api_view(['POST'])
# def addOrder(request):
#     """
#     Створити нове замовлення.
#     Очікує структуру даних:
#     {
#         "customer": <ID клієнта>,
#         "ticket": <ID квитка>,
#         "seller": <ID продавця>
#     }
#     """
#     serializer = OrderSerializer(data=request.data)
#
#     # Перевірка валідності даних
#     if serializer.is_valid():
#         # Перевірка унікальності квитка
#         ticket_id = serializer.validated_data['ticket'].id
#         if Order.objects.filter(ticket_id=ticket_id).exists():
#             return Response(
#                 {"error": "Цей квиток вже прив'язаний до існуючого замовлення."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         # Збереження замовлення
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#===== UPDATING
# @api_view(['PUT'])
# def updateOrder(request, pk):
#     """
#     Оновити існуюче замовлення.
#     Очікує структуру даних:
#     {
#         "customer": <ID клієнта>,
#         "ticket": <ID квитка>,
#         "seller": <ID продавця>
#     }
#     """
#     try:
#         # Отримуємо замовлення за ID
#         order = Order.objects.get(id=pk)
#     except Order.DoesNotExist:
#         return Response({"error": "Замовлення з вказаним ID не знайдено."}, status=status.HTTP_404_NOT_FOUND)

#     serializer = OrderSerializer(order, data=request.data)

#     if serializer.is_valid():
#         # Перевірка, чи квиток прив'язаний до іншого замовлення
#         new_ticket_id = serializer.validated_data['ticket'].id
#         if Order.objects.filter(ticket_id=new_ticket_id).exclude(id=pk).exists():
#             return Response(
#                 {"error": "Цей квиток вже прив'язаний до іншого замовлення."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         # Оновлення замовлення
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Customer
@api_view(['PUT'])
def updateCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomerSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Ticket
@api_view(['PUT'])
def updateTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
    except Ticket.DoesNotExist:
        return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = TicketSerializer(ticket, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update Seller
@api_view(['PUT'])
def updateSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = SellerSerializer(seller, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE ONE
# Видалення одного клієнта
@api_view(['DELETE'])
def deleteCustomer(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалити всі замовлення, пов'язані з цим клієнтом
    deleted_orders = Order.objects.filter(customer=customer).delete()

    # Видалити самого клієнта
    customer.delete()
    return Response({
        "message": f"Customer and {deleted_orders[0]} related orders successfully deleted."
    }, status=status.HTTP_200_OK)

# Видалення одного квитка
@api_view(['DELETE'])
def deleteTicket(request, pk):
    try:
        ticket = Ticket.objects.get(id=pk)
    except Ticket.DoesNotExist:
        return Response({"detail": "Ticket not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалити всі замовлення, пов'язані з цим квитком
    deleted_orders = Order.objects.filter(ticket=ticket).delete()

    # Видалити сам квиток
    ticket.delete()
    return Response({
        "message": f"Ticket and {deleted_orders[0]} related orders successfully deleted."
    }, status=status.HTTP_200_OK)

# Видалення одного продавця
@api_view(['DELETE'])
def deleteSeller(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалити всі замовлення, пов'язані з цим продавцем
    deleted_orders = Order.objects.filter(seller=seller).delete()

    # Видалити самого продавця
    seller.delete()
    return Response({
        "message": f"Seller and {deleted_orders[0]} related orders successfully deleted."
    }, status=status.HTTP_200_OK)

# Видалити одне замовлення
# @api_view(['DELETE'])
# def deleteOrder(request, pk):
#     try:
#         order = Order.objects.get(id=pk)
#     except Order.DoesNotExist:
#         return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

#     order.delete()
#     return Response({"message": f"Order with ID {pk} successfully deleted."}, status=status.HTTP_200_OK)

# # FILTER ORDERS
# @api_view(['GET'])
# def filterOrders(request):
#     # Отримуємо параметри фільтрації з запиту
#     seller_id = request.query_params.get('seller', None)
#     start_date = request.query_params.get('start_date', None)
#     end_date = request.query_params.get('end_date', None)

#     orders = Order.objects.all()

#     # Фільтрація за продавцем
#     if seller_id:
#         try:
#             seller_id = int(seller_id)  # Перетворюємо на ціле число
#             orders = orders.filter(seller_id=seller_id)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid seller ID'}, status=400)

#     # Фільтрація за датою
#     if start_date:
#         start_date = parse_datetime(start_date)
#         if not start_date:
#             return JsonResponse({'error': 'Invalid start date format'}, status=400)
#         orders = orders.filter(order_date__gte=start_date)

#     if end_date:
#         end_date = parse_datetime(end_date)
#         if not end_date:
#             return JsonResponse({'error': 'Invalid end date format'}, status=400)
#         orders = orders.filter(order_date__lte=end_date)

#     # Серіалізація та повернення результату
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)


# DELETE MANY
# Видалити багатьох клієнтів
# @api_view(['DELETE'])
# def deleteCustomers(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Customer.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} customers successfully deleted."}, status=status.HTTP_200_OK)

# # Видалити багато квитків
# @api_view(['DELETE'])
# def deleteTickets(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Ticket.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} tickets successfully deleted."}, status=status.HTTP_200_OK)

# # Видалити багатьох продавців
# @api_view(['DELETE'])
# def deleteSellers(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Seller.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} sellers successfully deleted."}, status=status.HTTP_200_OK)

# # Видалити багато замовлень
# @api_view(['DELETE'])
# def deleteOrders(request):
#     ids = request.data.get('ids', [])
#     if not ids:
#         return Response({"detail": "No IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

#     deleted_count, _ = Order.objects.filter(id__in=ids).delete()
#     return Response({"message": f"{deleted_count} orders successfully deleted."}, status=status.HTTP_200_OK)
def is_valid_image(file):
    # Перевірка формату файлу (JPEG, PNG, GIF)
    try:
        image = Image.open(file)
        if image.format in ['JPEG', 'PNG', 'GIF']:
            return True
        return False
    except Exception:
        return False


@api_view(['POST'])
def uploadSellerPhoto(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    if seller.photo != None:
        return Response({"detail": "To update photo use another request"}, status=status.HTTP_400_BAD_REQUEST)

    photo_file = request.FILES.get('photo')
    if not photo_file:
        return Response({"detail": "No photo provided."}, status=status.HTTP_400_BAD_REQUEST)

    # Перевірка формату файлу
    if not is_valid_image(photo_file):
        return Response({"detail": "Invalid file type. Only JPEG, PNG, and GIF are allowed."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Відкриваємо зображення
    image = Image.open(photo_file)

    # Якщо зображення має альфа-канал (прозорість), перетворюємо в RGB
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Створюємо потік для зображення
    img_io = io.BytesIO()

    # Обробка GIF зображення
    if image.format == 'GIF':
        image.save(img_io, format='GIF')
        img_io.seek(0)
        # Зберігаємо як GIF
        seller.photo = img_io.read()

    # Обробка PNG та JPEG
    else:
        image.save(img_io, format='JPEG')  # Зберігаємо як JPEG
        img_io.seek(0)
        seller.photo = img_io.read()

    seller.save()

    return Response({"detail": "Photo uploaded successfully."}, status=status.HTTP_200_OK)


@api_view(['GET'])
def getSellerPhoto(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    if not seller.photo:
        return Response({"detail": "No photo found."}, status=status.HTTP_404_NOT_FOUND)

    # Повертаємо фото відповідно до формату
    try:
        img_io = io.BytesIO(seller.photo)
        img_io.seek(0)  # Потрібно перемістити курсор на початок потоку після відкриття зображення

        # Якщо це GIF, просто відправляємо його без переробки
        if img_io.getvalue().startswith(b'GIF'):
            response = HttpResponse(img_io, content_type='image/gif')
        else:
            # Для інших форматів, наприклад JPEG чи PNG
            img_io.seek(0)  # Переміщуємо курсор потоку знову на початок
            response = HttpResponse(img_io, content_type='image/jpeg')  # Для JPEG, можливо, потрібно додати PNG
            response['Content-Type'] = 'image/jpeg'  # Використовуємо правильний Content-Type для JPEG
        return response
    except Exception:
        return Response({"detail": "Failed to process the photo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def updateSellerPhoto(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    photo_file = request.FILES.get('photo')
    if not photo_file:
        return Response({"detail": "No photo provided."}, status=status.HTTP_400_BAD_REQUEST)

    # Перевірка формату файлу
    if not is_valid_image(photo_file):
        return Response({"detail": "Invalid file type. Only JPEG, PNG, and GIF are allowed."}, status=status.HTTP_400_BAD_REQUEST)

    # Відкриваємо зображення
    image = Image.open(photo_file)

    # Якщо зображення має альфа-канал (прозорість), перетворюємо в RGB
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    # Створюємо потік для зображення
    img_io = io.BytesIO()

    # Обробка GIF зображення
    if image.format == 'GIF':
        image.save(img_io, format='GIF')
        img_io.seek(0)
        seller.photo = img_io.read()

    # Обробка PNG та JPEG
    else:
        image.save(img_io, format='JPEG')  # Зберігаємо як JPEG
        img_io.seek(0)
        seller.photo = img_io.read()

    seller.save()

    return Response({"detail": "Photo updated successfully."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteSellerPhoto(request, pk):
    try:
        seller = Seller.objects.get(id=pk)
    except Seller.DoesNotExist:
        return Response({"detail": "Seller not found."}, status=status.HTTP_404_NOT_FOUND)

    # Перевірка наявності зображення
    if not seller.photo:
        return Response({"detail": "No photo to delete."}, status=status.HTTP_400_BAD_REQUEST)

    seller.photo = None  # Видалення зображення
    seller.save()

    return Response({"detail": "Photo deleted successfully."}, status=status.HTTP_200_OK)

###############################################################################################
from django.conf import settings
from django.core.files.storage import default_storage

@api_view(['POST'])
def uploadCustomerPhoto(request, pk):
    try:
        # Припускаємо, що ви використовуєте модель Customer
        customer = Customer.objects.get(id=pk)
    except ObjectDoesNotExist:
        return Response({"detail": "Customer not found."}, status=404)

    # Перевіряємо, чи є фото в запиті
    photo_file = request.FILES.get('photo')
    if not photo_file:
        return Response({"detail": "No photo provided."}, status=400)

    if not is_valid_image(photo_file):
        return Response({"detail": "Invalid file type. Only JPEG, PNG, and GIF are allowed."},
                        status=status.HTTP_400_BAD_REQUEST)

    if customer.profile_photo != None:
        return Response({"detail": "Use another request UPDATE."}, status=400)

    # Створення шляху до файлу
    media_root = settings.MEDIA_ROOT
    customer_directory = os.path.join(media_root, 'customers')
    if not os.path.exists(customer_directory):
        os.makedirs(customer_directory)

    # Формуємо повний шлях до файлу
    full_path = os.path.join(customer_directory, f"{customer.id}_profile_photo.jpg")

    # Зберігаємо файл
    try:
        with default_storage.open(full_path, 'wb+') as destination:
            for chunk in photo_file.chunks():
                destination.write(chunk)
        # Оновлення даних користувача з шляхом до фото
        customer.profile_photo = full_path
        customer.save()

        return Response({"detail": "Photo uploaded successfully."}, status=200)
    except Exception as e:
        return Response({"detail": str(e)}, status=500)


from django.http import FileResponse

@api_view(['GET'])
def getCustomerPhoto(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    if not customer.profile_photo:
        return Response({"detail": "No photo found."}, status=status.HTTP_404_NOT_FOUND)



    # Повертаємо зображення з файлової системи
    full_path = os.path.join(settings.MEDIA_ROOT, customer.profile_photo)
    if os.path.exists(full_path):
        content_type = 'image/jpeg' if full_path.endswith('.jpg') else f'image/{full_path.split(".")[-1]}'
        return FileResponse(open(full_path, 'rb'), content_type=content_type)

    return Response({"detail": "File not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def updateCustomerPhoto(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    if customer.profile_photo is None:
        return Response({"detail": "Use another request ADD."}, status=400)

    photo_file = request.FILES.get('photo')
    if not photo_file:
        return Response({"detail": "No photo provided."}, status=status.HTTP_400_BAD_REQUEST)

    if not is_valid_image(photo_file):
        return Response({"detail": "Invalid file type. Only JPEG, PNG, and GIF are allowed."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Видалення старого фото
    if customer.profile_photo:
        old_path = os.path.join(settings.MEDIA_ROOT, customer.profile_photo)
        if os.path.exists(old_path):
            os.remove(old_path)

    # Генерація нового імені файлу
    filename = f'{pk}_profile_photo.{photo_file.name.split(".")[-1]}'
    file_path = os.path.join('customers', filename)

    # Зберігаємо нове фото
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    with default_storage.open(full_path, 'wb+') as destination:
        for chunk in photo_file.chunks():
            destination.write(chunk)

    # Оновлюємо шлях до файлу в базі даних
    customer.profile_photo = file_path
    customer.save()

    return Response({"detail": "Photo updated successfully."}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def deleteCustomerPhoto(request, pk):
    try:
        customer = Customer.objects.get(id=pk)
    except Customer.DoesNotExist:
        return Response({"detail": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    if not customer.profile_photo:
        return Response({"detail": "No photo to delete."}, status=status.HTTP_400_BAD_REQUEST)

    # Видалення фото з файлової системи
    full_path = os.path.join(settings.MEDIA_ROOT, customer.profile_photo)
    if os.path.exists(full_path):
        os.remove(full_path)

    # Очищення поля у базі даних
    customer.profile_photo = None
    customer.save()

    return Response({"detail": "Photo deleted successfully."}, status=status.HTTP_200_OK)







################ БРОКЕРИ ###########################
from .tasks import send_message_to_queue

# ОТРИМАТИ КОНКРЕТНЕ ЗАМОВЛЕННЯ
@api_view(['GET'])
def getOrder(request, pk):
    """
    API endpoint для отримання замовлення через брокер повідомлень
    """
    try:
        # Отримуємо дані з бази
        order = Order.objects.get(id=pk)
        # Серіалізуємо дані
        serializer = OrderSerializer(order)
        serialized_data = serializer.data
        
        # Формуємо повідомлення для черги з серіалізованими даними
        message = json.dumps({
            'action': 'get_order',
            'order_id': pk,
            'data': serialized_data
        }, cls=DjangoJSONEncoder)
        
        # Відправляємо повідомлення в чергу
        send_message_to_queue(message)
        
        # Повертаємо серіалізовані дані
        return Response(serialized_data)
        
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except json.JSONDecodeError as e:
        return Response({
            "error": f"JSON serialization error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            "error": f"Failed to process request: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ДОДАТИ ЗАМОВЛЕННЯ
@api_view(['POST'])
def addOrder(request):
    """
    Створити нове замовлення з відправкою повідомлення в RabbitMQ.
    """
    serializer = OrderSerializer(data=request.data)

    # Перевірка валідності даних
    if serializer.is_valid():
        # Перевірка унікальності квитка
        ticket_id = serializer.validated_data['ticket'].id
        if Order.objects.filter(ticket_id=ticket_id).exists():
            return Response(
                {"error": "Цей квиток вже прив'язаний до існуючого замовлення."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Збереження замовлення
        serializer.save()

        # Відправка повідомлення в RabbitMQ
        send_message_to_queue.delay(f"New order created with ID: {serializer.data['id']}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ОНОВИТИ ІСНУЮЧЕ ЗАМОВЛЕННЯ
@api_view(['PUT'])
def updateOrder(request, pk):
    """
    Оновити існуюче замовлення.
    Очікує структуру даних:
    {
        "customer": <ID клієнта>,
        "ticket": <ID квитка>,
        "seller": <ID продавця>
    }
    """
    try:
        # Отримуємо замовлення за ID
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"error": "Замовлення з вказаним ID не знайдено."}, status=status.HTTP_404_NOT_FOUND)

    serializer = OrderSerializer(order, data=request.data)

    if serializer.is_valid():
        # Перевірка, чи квиток прив'язаний до іншого замовлення
        new_ticket_id = serializer.validated_data['ticket'].id
        if Order.objects.filter(ticket_id=new_ticket_id).exclude(id=pk).exists():
            return Response(
                {"error": "Цей квиток вже прив'язаний до іншого замовлення."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Оновлення замовлення
        updated_order = serializer.save()

        # Відправка повідомлення про оновлення в RabbitMQ
        send_message_to_queue.delay(f"Order with ID {pk} updated.")

        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ВИДАЛИТИ ЗАМОВЛЕННЯ
@api_view(['DELETE'])
def deleteOrder(request, pk):
    """
    Видалити замовлення за ID і відправити повідомлення в RabbitMQ.
    """
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Видалення замовлення
    order.delete()

    # Відправка повідомлення в RabbitMQ через брокер
    send_message_to_queue.delay(f"Order with ID {pk} deleted.")

    return Response({"message": f"Order with ID {pk} successfully deleted."}, status=status.HTTP_200_OK)

# ОТРИМАТИ ВСІ ЗАМОВЛЕННЯ
@api_view(['GET'])
def getOrders(request):
    """
    API endpoint для отримання всіх замовлень через брокер повідомлень
    """
    try:
        # Отримуємо всі замовлення
        orders = Order.objects.all()
        # Серіалізуємо дані
        serializer = OrderSerializer(orders, many=True)
        serialized_data = serializer.data

        # Формуємо повідомлення для черги
        message = json.dumps({
            'action': 'get_all_orders',
            'data': serialized_data
        }, cls=DjangoJSONEncoder)
        
        # Відправляємо повідомлення в чергу
        send_message_to_queue(message)
        
        # Повертаємо серіалізовані дані
        return Response(serialized_data)
        
    except json.JSONDecodeError as e:
        return Response({
            "error": f"JSON serialization error: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response({
            "error": f"Failed to process request: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ВІДФІЛЬТРУВАТИ ЗАМОВЛЕННЯ
@api_view(['GET'])
def filterOrders(request):
    try:
        seller_id = request.query_params.get('seller', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)

        # Перевірка наявності хоча б одного з фільтрів
        if seller_id is None and (start_date is None or end_date is None):
            return Response(
                {"error": "Either 'seller' or both 'start_date' and 'end_date' parameters are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        filters = {}

        # Якщо передано 'seller', додаємо до фільтра
        if seller_id is not None:
            try:
                seller_id = int(seller_id)
                filters['seller_id'] = seller_id
            except ValueError:
                return Response(
                    {"error": "Invalid seller ID format"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Якщо передано 'start_date' та 'end_date', додаємо до фільтра
        if start_date is not None and end_date is not None:
            filters['start_date'] = start_date
            filters['end_date'] = end_date

        # Отримуємо замовлення з фільтрами
        orders = Order.objects.all()

        if 'seller_id' in filters:
            orders = orders.filter(seller_id=filters['seller_id'])

        if 'start_date' in filters and 'end_date' in filters:
            # Фільтрація за полем 'order_date', якщо воно відповідає даті створення
            orders = orders.filter(
                order_date__gte=start_date,
                order_date__lte=end_date
            )

        if not orders.exists():
            return Response(
                {"error": "No orders found for the given filters"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Серіалізація результатів
        serializer = OrderSerializer(orders, many=True)
        
        # Відправляємо повідомлення в чергу для логування
        message = json.dumps({
            'action': 'get_orders_by_filter',
            'filters': filters,
            'data': serializer.data
        }, cls=DjangoJSONEncoder)
        
        send_message_to_queue(message)
        
        return Response(serializer.data)

    except Exception as e:
        return Response({
            "error": f"Failed to process request: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
