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


@register.filter
def add_ngModel(field, arg):
    if arg is None:
        return field

    field.field.widget.attrs.update({"ng-model": arg})

    return field


@register.filter
def add_ngChange(field, arg):
    if arg is None:
        return field

    field.field.widget.attrs.update({"ng-change": arg})

    return field


@register.filter
def add_ngModelOptions(field, arg):
    if arg is None:
        return field

    field.field.widget.attrs.update({"ng-model-options": arg})

    return field


@register.filter
def set_rows(field, arg):
    if arg is None:
        return field

    field.field.widget.attrs.update({"rows": arg})

    return field
