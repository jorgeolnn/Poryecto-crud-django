from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.http import Http404, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Permission
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile, Producto, Product, CartItem, Categoria, Resena
from .forms import ProfileForm, UserUpdateForm, ProfileUpdateForm, ProductoForm, ContactoForm, UserPermissionForm, ComentarioForm, UpdateComentarioForm
from django.core.paginator import Paginator
# Create your views here.
def home(request):

    return render(request, "productos/home.html")

# 

def Tienda(request):
    categoria_id = request.GET.get('categoria')  # Obtener el ID de la categoría desde la URL
    if categoria_id:
        productos = Producto.objects.filter(categoria_id=categoria_id)  # Filtrar por categoría
    else:
        productos = Producto.objects.all()  # Mostrar todos los productos si no hay filtro

    categorias = Categoria.objects.all()  # Obtener todas las categorías para el filtro

    return render(request, 'productos/Tienda.html', {
        'entity': productos,
        'categorias': categorias,
    })

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
            producto = formulario.save(commit=False)  # No guardar aún
            producto.usuario = request.user  # Asignar el producto al usuario autenticado
            producto.save()  # Ahora guardar
            messages.success(request, "Producto registrado")
            return redirect('agregar_producto')  # Redirige después de guardar
    else:
        formulario = ProductoForm()
    return render(request, 'agregacion/agregar.html', {'form': formulario})


def listar_productos(request):
    if request.user.is_superuser:
        productos = Producto.objects.all()
    else:
        productos = Producto.objects.filter(usuario=request.user)

    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(productos, 5)
        productos = paginator.page(page)
    except:
        raise Http404

    data = {
        'entity': productos,
        'paginator': paginator,
        'is_admin': request.user.is_superuser
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


@permission_required('auth.change_user')
def manage_permissions(request):
    if request.method == 'POST':
        form = UserPermissionForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            permissions = form.cleaned_data['permissions']
            # Actualizar los permisos del usuario
            user.user_permissions.set(permissions)
            user.save()
            messages.success(request, "Permisos Otorgados Correctamente")
            return redirect('manage_permissions')  # Redirige a la misma página o a una página de éxito
    else:
        form = UserPermissionForm()
    
    return render(request, 'productos/manage_permissions.html', {'form': form})

def obtener_productos_del_carrito(request):
    carrito = request.session.get('carrito', {})  # Asumiendo que guardas el carrito en la sesión
    productos = []
    
    for producto_id, cantidad in carrito.items():
        producto = Producto.objects.get(id=producto_id)  # Asegúrate de manejar excepciones aquí
        producto.cantidad = cantidad  # Agregamos la cantidad al objeto del producto
        productos.append(producto)

    return productos

def detalle_compra(request):
    # Suponiendo que tienes una forma de obtener los productos del carrito
    productos = obtener_productos_del_carrito(request)  # Asegúrate de implementar esta función
    total_compra = sum(producto.precio * producto.cantidad for producto in productos)  # Ajusta según tu lógica

    context = {
        'productos': productos,
        'total_compra': total_compra,
    }
    return render(request, 'compra/detalle_compra.html', context)

@login_required
def agregar_comentario(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.producto = producto
            comentario.usuario = request.user
            comentario.save()
            return redirect('detalle_producto', producto_id=producto.id)  # Cambia según tu vista de detalle
    else:
        form = ComentarioForm()

    return render(request, 'productos/agregar_comentario.html', {'form': form, 'producto': producto})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    resenas = Resena.objects.filter(producto=producto).order_by('-fecha_creacion')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                nueva_resena = form.save(commit=False)
                nueva_resena.producto = producto
                nueva_resena.usuario = request.user  # Asigna el usuario autenticado
                nueva_resena.save()
                messages.success(request, "Se guardó el comentario!!")
                return redirect('detalle_producto', producto_id=producto_id)
        else:
            # Redirigir al login si el usuario no está autenticado
            return redirect('login')  # Ajusta la URL del login según tu configuración

    else:
        form = ComentarioForm()

    return render(request, 'compra/detalle_producto.html', {
        'producto': producto,
        'resenas': resenas,
        'form': form
    })

@login_required
def eliminar_comentario(request, id, producto_id):
    # Obtener el comentario por su ID
    resena = get_object_or_404(Resena, id=id)

    # Comprobar si el usuario autenticado es el autor del comentario o un administrador
    if request.user == resena.usuario or request.user.is_superuser:
        resena.delete()
        messages.success(request, 'El comentario ha sido eliminado con éxito.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este comentario.')

    # Redirigir de vuelta a la página del producto
    return redirect('detalle_producto', producto_id=producto_id)


@login_required
def editar_comentario(request, id, producto_id):
    resena = get_object_or_404(Resena, id=id)

    data = {
        'form': UpdateComentarioForm(instance=resena),
        'producto_id': producto_id
    }

    if request.method == 'POST':
        formulario = UpdateComentarioForm(request.POST, instance=resena)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Se cambió el comentario!!")
            return redirect(to="detalle_producto",  producto_id=producto_id)
        data["form"] = formulario

    return render(request, 'compra/editar_comentario.html', data)
