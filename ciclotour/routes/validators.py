from django.core.exceptions import ValidationError


def validate_latitude(value):
    if value > 90.00000000 or value < -90.00000000:
        raise ValidationError('Latitude must be in range -90;90')

def validate_longitude(value):
    if value > 180.00000000 or value < -180.00000000:
        raise ValidationError('Longitude must be in range -180;180')