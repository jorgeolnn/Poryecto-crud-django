from django.urls import path, include

from productos import views
from .views import registro, profile, profile_edit, agregar_producto, listar_productos, modificar_producto, eliminar_producto, detalle_producto,  manage_permissions

urlpatterns = [
   
    path('',views.home, name="home"),
    path('Tienda/', views.Tienda, name="Tienda"),
    path('servicio',views.servicio, name="servicio"),
    path('Contacto',views.Contacto, name="Contacto"),
    path('login',views.login, name="login"),
    path('registro/',registro, name="registro"),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('agregar-producto/', agregar_producto, name='agregar_producto'),
    path('listar-productos/', listar_productos, name='listar_productos'),
    path('modificar-producto/<id>/', modificar_producto, name='modificar_producto'),
    path('eliminar-producto/<id>/', eliminar_producto, name='eliminar_producto'),
    path('detalle_compra/', views.detalle_compra, name="detalle_compra"),
   
    path('detalle-producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('manage-permissions/', manage_permissions, name='manage_permissions'),
    

]


   