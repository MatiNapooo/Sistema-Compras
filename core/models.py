from django.db import models
import uuid
from django.contrib.auth.models import User

class Compra(models.Model):
    TIPO_CHOICES = [
        ('INSUMO', 'Insumo'),
        ('PAPEL', 'Papel'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    pedido_por = models.CharField(max_length=100)
    # Legacy fields — kept for backward compatibility with old single-item orders
    insumo = models.CharField(max_length=200, blank=True, default='')
    proveedor = models.CharField(max_length=200)
    marca = models.CharField(max_length=100, blank=True, default='')
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    pagado = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.insumo:
            return f"{self.tipo} - {self.insumo} ({self.fecha})"
        return f"{self.tipo} - {self.proveedor} ({self.fecha})"

    @property
    def precio_total(self):
        """Devuelve el precio total: suma de ítems si los hay, o precio legacy."""
        items = self.items.all()
        if items.exists():
            return sum(item.subtotal for item in items)
        return self.precio or 0


class ItemCompra(models.Model):
    """Línea de detalle de una compra multi-insumo."""
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='items')
    insumo = models.CharField(max_length=200)
    marca = models.CharField(max_length=100, blank=True, default='')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.insumo} x{self.cantidad} — {self.compra}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    @property
    def photo_url(self):
        """
        Devuelve la URL de la imagen desde Cloudinary.
        El campo 'image' guarda el public_id, ej: 'profile_pics/marcelo'
        """
        CLOUD_NAME = 'dvinasjl9'

        if self.image and self.image.name and self.image.name != 'default.jpg':
            public_id = self.image.name
            return f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/{public_id}"

        # Imagen por defecto: un avatar genérico de Cloudinary
        return f"https://res.cloudinary.com/{CLOUD_NAME}/image/upload/profile_pics/default_avatar"


class TrustedDevice(models.Model):
    """Token persistente para recordar el dispositivo del usuario."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trusted_devices')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"TrustedDevice({self.user.username}, expires={self.expires_at})"

