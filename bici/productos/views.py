from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile, Producto, Product, CartItem
from .forms import ProfileForm, UserUpdateForm, ProfileUpdateForm, ProductoForm, ContactoForm
from django.core.paginator import Paginator
# Create your views here.
def home(request):

    return render(request, "productos/home.html")

# 
def Tienda(request):
    productos = Producto.objects.all()
    data = {
        'productos': productos
    }
    return render(request, "productos/Tienda.html", data)

#
def servicio(request):

    return render(request, "productos/servicio.html")

#
def Contacto(request):
    data = {
        'form': ContactoForm()
    }

    if request.method =='POST':
        formulario = ContactoForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Contacto enviado")
        else:
            data["form"] = formulario
    return render(request, "productos/Contacto.html", data)

# Vistas de registro y perfil
def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)  # Aquí es donde se produce la autenticación
            messages.success(request, "Te registraste correctamente")
            return redirect(to="home")
        data["form"] = formulario
    return render(request, 'registration/registro.html', data)

#
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'registration/profile.html', {
        'form': form
    })

#
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Perfil actualizado correctamente")
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'registration/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

###########

    
@permission_required('productos.add_producto')
def agregar_producto(request):
    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Producto registrado")
            return redirect('agregar_producto')  # Redirige después de guardar
    else:
        formulario = ProductoForm()
    return render(request, 'agregacion/agregar.html', {'form': formulario})


@permission_required('productos.view_producto')
def listar_productos(request):
    productos = Producto.objects.all()
    page = request.GET.get('page', 1)
       # data = {
    #     'productos': productos
    # }
    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator
    }
    return render(request, 'agregacion/listar.html', data)


@permission_required('productos.change_producto')
def modificar_producto(request, id):

    producto = get_object_or_404(Producto, id=id)

    data = {

        'form': ProductoForm(instance=producto)
    }

    if request.method == 'POST':
        formulario = ProductoForm(data=request.POST, instance=producto, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado correctamente")
            return redirect(to="listar_productos")
        data["form"] = formulario
        

    return render(request, 'agregacion/modificar.html', data)


@permission_required('productos.delete_producto')
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, "Eliminado correctamente")
    return redirect(to="listar_productos")

#
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'compra/detalle_producto.html', {'producto': producto})

#Carrito de compra



