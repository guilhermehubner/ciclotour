from ciclotour.routes.models import FieldKind, PointKind
from django.contrib import admin


class PointKindModelAdmin(admin.ModelAdmin):
    list_display = ['kind', 'icon_img']

    def icon_img(self, obj):
        return '<img width="32px" src="{}">'.format(obj.icon.url)

    icon_img.allow_tags = True
    icon_img.short_description = 'Icon'


admin.site.register(FieldKind)
admin.site.register(PointKind, PointKindModelAdmin)