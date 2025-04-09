from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """"Dictionary ichidan qiymat olish"""
    return dictionary.get(key, 0)