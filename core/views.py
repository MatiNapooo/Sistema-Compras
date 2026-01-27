from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import json
import urllib.request
import re
from .models import Compra
from django.http import JsonResponse
from datetime import datetime, timedelta

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

    # Fetch recent orders (last 3)
    recent_orders = Compra.objects.all().order_by('-fecha')[:3]

    return render(request, 'core/dashboard.html', {
        'dolar': dolar_oficial,
        'recent_orders': recent_orders
    })

@login_required(login_url='/')
@login_required(login_url='/')
def registrar_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Create new purchase
            created_compra = Compra.objects.create(
                usuario=request.user,
                tipo=data.get('tipo', 'INSUMO'), # Use provided type or default
                pedido_por=request.user.first_name if request.user.first_name else request.user.username,
                insumo=data.get('insumo'),
                proveedor=data.get('proveedor'),
                marca=data.get('marca'),
                precio=data.get('precio'),
                observaciones=data.get('observaciones')
            )
            return JsonResponse({'status': 'success', 'id': created_compra.id})
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

@login_required(login_url='/')
def orden_compra_view(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    
    # Defaults
    parsed_data = {
        'tipo': compra.insumo,
        'ancho': '-',
        'alto': '-',
        'gramaje': '-',
        'qty': 1,
        'unit_price': compra.precio,
        'is_paper': False
    }

    # Regex Parsing for Paper: "Papel [Type] [W]x[H] [G]gr (x[Qty])"
    # Example: Papel Ilustracion 72x102 275gr (x12)
    match = re.search(r"Papel (.+) (\d+)x(\d+) (\d+)gr \(x(\d+)\)", compra.insumo)
    
    # Determine if it is paper based on Type OR Regex match (for backward compatibility)
    if compra.tipo == 'PAPEL' or match:
        parsed_data['is_paper'] = True
        
    if match:
        parsed_data['tipo'] = match.group(1)
        parsed_data['ancho'] = match.group(2)
        parsed_data['alto'] = match.group(3)
        parsed_data['gramaje'] = match.group(4)
        parsed_data['qty'] = int(match.group(5))
        if parsed_data['qty'] > 0:
            parsed_data['unit_price'] = compra.precio / parsed_data['qty']
            
    # Generic Insumo Parsing: "Item Name (xQty)"
    # Fallback if not Paper but has quantity suffix
    elif not parsed_data['is_paper']:
        match_generic = re.search(r"(.+) \(x(\d+)\)$", compra.insumo)
        if match_generic:
            parsed_data['tipo'] = match_generic.group(1)
            parsed_data['qty'] = int(match_generic.group(2))
            if parsed_data['qty'] > 0:
                parsed_data['unit_price'] = compra.precio / parsed_data['qty']

    # Calculations
    # Ensure precio is treated as a number (it might come as a string/decimal from DB)
    subtotal = float(compra.precio)
    iva = subtotal * 0.21
    total_final = subtotal + iva

    context = {
        'compra': compra,
        'parsed': parsed_data,
        'iva': iva,
        'total_final': total_final,
        'fecha_hoy': datetime.now()
    }
    return render(request, 'core/orden_compra.html', context)

@login_required(login_url='/')
def delete_compra(request, compra_id):
    if request.method == 'POST':
        compra = get_object_or_404(Compra, id=compra_id)
        compra.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

@login_required(login_url='/')
def ordenes_list_view(request):
    # Fetch all orders
    all_orders = Compra.objects.all().order_by('-fecha')
    
    # Filter by type
    insumos = all_orders.filter(tipo='INSUMO')
    papeles = all_orders.filter(tipo='PAPEL')
    
    context = {
        'insumos': insumos,
        'papeles': papeles
    }
    return render(request, 'core/ordenes_lista.html', context)

@login_required(login_url='/')
def historial_view(request):
    # Get query parameters
    query = request.GET.get('q', '')
    provider = request.GET.get('provider', '')
    months = request.GET.get('months', '')
    
    results = []
    
    if request.method == 'GET' and (query or provider or months):
        orders = Compra.objects.all().order_by('-fecha')
        
        # Filter by Time
        if months and months != 'all':
            try:
                days = int(months) * 30
                start_date = datetime.now() - timedelta(days=days)
                orders = orders.filter(fecha__gte=start_date)
            except ValueError:
                pass # Ignore invalid month values
        
        # Filter by Query (Insumo/Papel Name)
        if query:
            orders = orders.filter(insumo__icontains=query)
            
        # Filter by Provider
        if provider:
            orders = orders.filter(proveedor__icontains=provider)
            
        results = orders

    context = {
        'results': results,
        'query': query,
        'provider': provider,
        'months': months
    }
    return render(request, 'core/historial.html', context)