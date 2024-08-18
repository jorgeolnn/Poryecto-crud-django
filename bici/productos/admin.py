from django.contrib import admin
from .models import Profile, Marca, Producto, Contacto
from .forms import ProductoForm


# Register your models here.
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'descripcion', 'nuevo', 'marca', 'fecha_fabricacion', 'usuario')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(usuario=request.user)
        return qs
    list_editable = ["precio"]
    search_fields = ["nombre"]
    list_filter = ["marca", "nuevo"]
    list_per_page = 5
    form = ProductoForm

admin.site.register(Profile)
admin.site.register(Marca)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Contacto)

