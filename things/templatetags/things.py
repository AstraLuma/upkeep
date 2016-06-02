from django import template
from ..models import Thing

register = template.Library()

@register.simple_tag
def things(user):
    return Thing.objects.filter(user=user)