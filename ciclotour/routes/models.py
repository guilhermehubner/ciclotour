from ciclotour.routes.validators import validate_latitude, validate_longitude
from django.db  import models


class FieldKind(models.Model):
    kind = models.CharField(max_length=50)


class WayPoint(models.Model):
    INITIAL = 'I'
    LINEAR = 'L'
    GOOGLE = 'G'
    KINDS = (
        (INITIAL, 'Inicial'),
        (LINEAR, 'Linear'),
        (GOOGLE, 'Google')
    )

    route = models.ForeignKey('Route')
    kind = models.CharField(max_length=1, choices=KINDS)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, validators=[validate_latitude,])
    longitude = models.DecimalField(max_digits=11, decimal_places=8, validators=[validate_longitude,])


class Route(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('core.CustomUser')
    field = models.ForeignKey('FieldKind')
