# productos/models.py
from django.db import models
from django.contrib.auth.models import User

# Registro de usuarios, perfiles y login.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    residencia = models.CharField(max_length=255, choices=[('chile', 'Chile'), ('argentina', 'Argentina'), ('españa', 'España'), ('colombia', 'Colombia')], blank=True, null=True)
    estado_civil = models.CharField(max_length=50, choices=[('soltero', 'Soltero'), ('casado', 'Casado'), ('divorciado', 'Divorciado'), ('viudo', 'Viudo')], blank=True, null=True)

    def __str__(self):
        return self.user.username

##################################

class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.TextField()
    nuevo = models.BooleanField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, default=1)
    fecha_fabricacion = models.DateField()
    imagen = models.ImageField(upload_to="productos", null=True)
    stock = models.IntegerField(default=0, verbose_name='Stock')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  # Relación con el usuario
    def __str__(self):
        return self.nombre



##############
opciones_consultas = [
    [0, "consulta"],
    [1, "Reclamo"],
    [2, "Sugerencia"],
    [3, "Felicitaciones"]


]
 

class Contacto(models.Model):
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    tipo_consulta = models.IntegerField(choices=opciones_consultas)
    mensaje = models.TextField()
    avisos = models.BooleanField()

    def __str__(self):
        return self.nombre

#carrito

class Product(models.Model):       #########################no me sirvió
    nombre = models.CharField(max_length=255)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to="productos", null=True)

    def __str__(self):
        return self.nombre

class CartItem(models.Model):
    producto = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"


###########################################3333
class Resena(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario de {self.usuario.username} sobre {self.producto.nombre}"