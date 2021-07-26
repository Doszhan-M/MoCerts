
from django import template
from ..models import PreviewSettings
from django.conf import settings


register = template.Library()


@register.filter(name='property')
def property(value):
    '''для фильтрации превью страниц'''

    if PreviewSettings.objects.exists():
        preview_settings = PreviewSettings.objects.all().first()
    else:
        PreviewSettings.objects.create()
        preview_settings = PreviewSettings.objects.all().first()
    
    property_values = {
        'type': preview_settings.type,
        'site_name': preview_settings.site_name,
        'title': preview_settings.title,
        'description': preview_settings.description,
        'locale': preview_settings.locale,
        'twitter_creator': preview_settings.twitter_creator,
        'url': preview_settings.url,
        'image': preview_settings.image,
        }

    if value == 'type':
        value = property_values['type']
    elif value == 'site_name':
        value = property_values['site_name']
    elif value == 'title':
        value = property_values['title']
    elif value == 'description':
        value = property_values['description']
    elif value == 'locale':
        value = property_values['locale']
    elif value == 'twitter_creator':
        value = property_values['twitter_creator']
    elif value == 'url':
        value = property_values['url']
    elif value == 'image':
        value = property_values['image']
    return value


