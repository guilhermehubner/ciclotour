from django import template

register = template.Library()


@register.filter
def set_placeholder_as_label(field):
    field.field.widget.attrs.update({"placeholder": field.label})
    return field

@register.filter
def add_class(field, arg):
    if arg is None:
        return field

    field.field.widget.attrs.update({"class": arg})

    return field