from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
import urllib.request
from .models import Compra
from django.http import JsonResponse
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        # 1. Obtener datos del formulario
        usuario_form = request.POST.get('username')
        clave_form = request.POST.get('password')
        
        # 2. Verificar credenciales con Django
        user = authenticate(request, username=usuario_form, password=clave_form)
        
        if user is not None:
            # 3. Si existe, iniciar sesión y redirigir al menú
            login(request, user)
            return redirect('dashboard')
        else:
            # Si falla, volvemos a mostrar el login con un mensaje de error (opcional)
            return render(request, 'core/login.html', {'error': 'Datos incorrectos'})

    # Si es GET (al entrar por primera vez)
    return render(request, 'core/login.html')

# Agregamos este decorador para proteger el menú:
# Si alguien intenta entrar directo sin loguearse, lo patea al login.
@login_required(login_url='/') 
def dashboard_view(request):
    dolar_oficial = {'compra': 0, 'venta': 0}
    try:
        url = 'https://dolarapi.com/v1/dolares/oficial'
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            dolar_oficial['compra'] = data.get('compra', 0)
            dolar_oficial['venta'] = data.get('venta', 0)
    except Exception as e:
        print(f"Error fetching dolar: {e}")

    # Fetch recent orders (last 5)
    recent_orders = Compra.objects.all().order_by('-fecha')[:5]

    return render(request, 'core/dashboard.html', {
        'dolar': dolar_oficial,
        'recent_orders': recent_orders
    })

@login_required(login_url='/')
def registrar_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create new purchase
            Compra.objects.create(
                usuario=request.user,
                tipo='INSUMO', # For now, hardcoded as we are in insumo form
                pedido_por=request.user.first_name if request.user.first_name else request.user.username,
                insumo=data.get('insumo'),
                proveedor=data.get('proveedor'),
                marca=data.get('marca'),
                precio=data.get('precio'),
                observaciones=data.get('observaciones')
            )
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

def logout_view(request):
    logout(request) # Cierra la sesión
    return redirect('login') # Lo manda a la pantalla de entrada

@login_required(login_url='/')
def nueva_compra_view(request):
    return render(request, 'core/nueva_compra_selection.html')

@login_required(login_url='/')
def compra_insumo_view(request):
    return render(request, 'core/compra_insumo.html')

@login_required(login_url='/')
def compra_papel_view(request):
    dolar_oficial = {'venta': 0}
    try:
        url = 'https://dolarapi.com/v1/dolares/oficial'
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            dolar_oficial['venta'] = data.get('venta', 0)
    except Exception as e:
        print(f"Error fetching dolar: {e}")

    return render(request, 'core/compra_papel.html', {'dolar': dolar_oficial})