from datetime import datetime

from ciclotour.routes.validators import validate_latitude, validate_longitude
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models


def _pointkind_icon_directory_path(instance, filename):
    file_extension = filename.split('.')[-1]
    return 'pointkind/icons/icon_{}.{}'.format(instance.kind, file_extension)


def _route_picture_directory_path(instance, filename):
    file_extension = filename.split('.')[-1]
    return 'routes/{}/pictures/routePic.{}'.format(instance.route.pk, file_extension)


class RoutePicture(models.Model):
    route = models.ForeignKey('Route')
    owner = models.ForeignKey('core.CustomUser')
    image = models.ImageField(upload_to= _route_picture_directory_path, max_length=255)
    description = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-id']


class Point(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    address = models.CharField(max_length=255)
    kind = models.ForeignKey('PointKind')
    latitude = models.DecimalField(max_digits=17, decimal_places=15, validators=[validate_latitude, ])
    longitude = models.DecimalField(max_digits=18, decimal_places=15, validators=[validate_longitude, ])
    route = models.ForeignKey('Route')


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
    FINAL_GOOGLE = 'FG'
    FINAL_LINEAR = 'FL'
    KINDS = (
        (INITIAL, 'Inicial'),
        (LINEAR, 'Linear'),
        (GOOGLE, 'Google'),
        (FINAL_GOOGLE, 'Final Google'),
        (FINAL_LINEAR, 'Final Linear')
    )

    route = models.ForeignKey('Route')
    kind = models.CharField(max_length=2, choices=KINDS)
    latitude = models.DecimalField(max_digits=17, decimal_places=15, validators=[validate_latitude, ])
    longitude = models.DecimalField(max_digits=18, decimal_places=15, validators=[validate_longitude, ])


class Route(models.Model):
    title = models.CharField(max_length=255)
    origin = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey('core.CustomUser')
    field = models.ForeignKey('FieldKind')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def get_picture(self):
        picture = self.routepicture_set.first()
        if picture:
            return picture.image.url
        return static('img/non_route_picture.png')

    def __str__(self):
        return self.title
