from django.db import models

class Organization(models.Model):
    name = models.CharField(max_length=120, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        from dispositivos.models import Zone  # Importamos aquí para evitar la importación circular
        # Lógica para asignar la zona a la organización si es necesario
        super(Organization, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
