from django import template

register = template.Library()

@register.filter(name='es_magistrado')
def es_magistrado(user):
    return user.tipo_usuario == 'MAG' if user.is_authenticated else False 