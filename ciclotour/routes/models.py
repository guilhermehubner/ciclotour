from ciclotour.routes.validators import validate_latitude, validate_longitude
from django.db  import models


def _pointkind_icon_directory_path(instance, filename):
    file_extension = filename.split('.')[-1]
    return 'pointkind/icons/icon_{}.{}'.format(instance.kind, file_extension)


class PointKind(models.Model):
    kind = models.CharField(max_length=50, unique=True)
    icon = models.ImageField(upload_to=_pointkind_icon_directory_path, max_length=255)

    def __str__(self):
        return self.kind


class Polyline(models.Model):
    route = models.ForeignKey('Route')
    encoded_polyline = models.CharField(max_length=1300)


class FieldKind(models.Model):
    kind = models.CharField(max_length=50)

    def __str__(self):
        return self.kind


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
    latitude = models.DecimalField(max_digits=17, decimal_places=15, validators=[validate_latitude,])
    longitude = models.DecimalField(max_digits=18, decimal_places=15, validators=[validate_longitude,])


class Route(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('core.CustomUser')
    field = models.ForeignKey('FieldKind')
