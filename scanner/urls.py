from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scan/<str:barcode>/', views.scan_barcode, name='scan_barcode'),
    path('auto_scan/', views.auto_scan_barcode, name='auto_scan_barcode'),
]
