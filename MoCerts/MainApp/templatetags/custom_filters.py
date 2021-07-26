
from django import template



register = template.Library()


# для фильтрации превью страниц
@register.filter(name='property')
def property(value):
    value = 'проверка'
    return value


