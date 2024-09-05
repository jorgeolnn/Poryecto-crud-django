from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Producto, Contacto
from django import forms
from .validators import MaxSizeFileValidator
from django.forms import ValidationError
from django.core.validators import FileExtensionValidator

# from PIL import Image
# Registro de usuarios, perfil, login.
class CustomUserCreationForm(UserCreationForm): 
    
    class Meta:
        
        model = User
        fields = ['username', "first_name", "last_name", "email", "password1", "password2"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']

# productos/forms.py


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['residencia', 'estado_civil']

################################################

# def validar_extension_imagen(field_file):
#     if field_file:
#         extensión = field_file.name.split('.')[-1].lower()
#         if extensión not in ['jpg', 'png', 'jpeg']:
#             raise ValidationError('Formato de imagen no permitido')


    
# def validar_dimensiones_imagen(field_file):
#     imagen = Image.open(field_file)
#     ancho, alto = imagen.size
    
#     # Validar dimensiones
#     if ancho < 800 or alto < 600:
#         raise ValidationError('La imagen debe tener un ancho mínimo de 800px y un alto mínimo de 600px')


class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(min_length=3, max_length=50)
    imagen = forms.ImageField(validators=[MaxSizeFileValidator(max_file_size=2), FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'], message="Solo se permiten archivos con extensiones .jpg, .png o .jpeg")])
    precio = forms.IntegerField(min_value=1, max_value=1500000)

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"]
        existe = Producto.objects.filter(nombre__iexact=nombre).exists()
        if existe:
            raise ValidationError("Este nombre ya existe")
        return nombre

    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'nuevo', 'marca', 'stock','fecha_fabricacion', 'imagen']
        widgets = {
            "fecha_fabricacion": forms.SelectDateWidget()
        }


##
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        #fields = ["nombre", "correo", "tipo_consulta", "mensaje", "avisos"]
        fields = '__all__' 

##CARRITO 

