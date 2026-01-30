
from django.contrib import admin
from django.urls import path
from core import views


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'), # Ruta raíz
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('nueva-compra/', views.nueva_compra_view, name='nueva_compra'),
    path('nueva-compra/insumo/', views.compra_insumo_view, name='compra_insumo'),
    path('nueva-compra/papel/', views.compra_papel_view, name='compra_papel'),
    path('registrar-compra/', views.registrar_compra, name='registrar_compra'),
    path('orden-compra/<int:compra_id>/', views.orden_compra_view, name='orden_compra'),
    path('eliminar-orden/<int:compra_id>/', views.delete_compra, name='delete_compra'),
    path('ordenes/', views.ordenes_list_view, name='ordenes_lista'),
    path('historial/', views.historial_view, name='historial'),
    path('toggle-payment-status/<int:compra_id>/', views.toggle_payment_status, name='toggle_payment_status'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)