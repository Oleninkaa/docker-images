from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
     # Customer paths
    path('customers/', views.getCustomers, name='get_customers'),
    path('customers/create', views.addCustomer, name='add_customer'),
    path('customers/read/<int:pk>/', views.getCustomer, name='get_customer'),
    path('customers/update/<int:pk>/', views.updateCustomer, name='update_customer'),
    path('customers/delete/<int:pk>/', views.deleteCustomer, name='delete_customer'),

    # Ticket paths
    path('tickets/', views.getTickets, name='get_tickets'),
    path('tickets/create', views.addTicket, name='add_ticket'),
    path('tickets/read/<int:pk>/', views.getTicket, name='get_ticket'),
    path('tickets/update/<int:pk>/', views.updateTicket, name='update_ticket'),
    path('tickets/delete/<int:pk>/', views.deleteTicket, name='delete_ticket'),

    # Seller paths
    path('sellers/', views.getSellers, name='get_sellers'),
    path('sellers/create', views.addSeller, name='add_seller'),
    path('sellers/read/<int:pk>/', views.getSeller, name='get_seller'),
    path('sellers/update/<int:pk>/', views.updateSeller, name='update_seller'),
    path('sellers/delete/<int:pk>/', views.deleteSeller, name='delete_seller'),

    # Order paths
    path('orders/', views.getOrders, name='get_orders'),
    path('orders/create', views.addOrder, name='add_order'),
    path('orders/read/<int:pk>/', views.getOrder, name='get_order'),
    path('orders/update/<int:pk>/', views.updateOrder, name='update_order'),
    path('orders/delete/<int:pk>/', views.deleteOrder, name='delete_order'),

    # Filter orders by date or seller
    path('orders/filter/', views.filterOrders, name='get_orders_by_seller'),


    path('sellers/<int:pk>/upload-photo/', views.uploadSellerPhoto, name='upload-seller-photo'),
    path('sellers/<int:pk>/photo/', views.getSellerPhoto, name='get-seller-photo'),
    path('seller/<int:pk>/photo/update/', views.updateSellerPhoto, name='update_seller_photo'),
    path('seller/<int:pk>/photo/delete/', views.deleteSellerPhoto, name='delete_seller_photo'),

    path('customers/<int:pk>/upload-photo/', views.uploadCustomerPhoto, name='upload_customer_photo'),
    path('customers/<int:pk>/photo/', views.getCustomerPhoto, name='get_customer_photo'),
    path('customers/<int:pk>/update-photo/', views.updateCustomerPhoto, name='update_customer_photo'),
    path('customers/<int:pk>/delete-photo/', views.deleteCustomerPhoto, name='delete_customer_photo'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)