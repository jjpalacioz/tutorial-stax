from django.db import models


class Compra(models.Model):
    """Modelo simple para registrar compras de la tienda."""
    producto = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creada_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.producto} x{self.cantidad}"

    @property
    def total(self):
        return self.cantidad * self.precio_unitario
