from django.db import models
from django.contrib.auth.models import User

class Compra(models.Model):
    TIPO_CHOICES = [
        ('INSUMO', 'Insumo'),
        ('PAPEL', 'Papel'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    pedido_por = models.CharField(max_length=100)
    insumo = models.CharField(max_length=200) # Nombre del item
    proveedor = models.CharField(max_length=200)
    marca = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.insumo} ({self.fecha})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
