from django import template
from ..models import Thing

register = template.Library()

@register.simple_tag
def get_things_for(user):
	if user.is_authenticated():
		return Thing.objects.filter(user=user)