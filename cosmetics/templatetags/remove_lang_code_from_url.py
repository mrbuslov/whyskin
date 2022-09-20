from django import template 
register = template.Library()

@register.filter
def remove_lang_code_from_url(value):
    return value.replace("/ru/","/")