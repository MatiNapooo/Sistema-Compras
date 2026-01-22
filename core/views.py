from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

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
    return render(request, 'core/dashboard.html')