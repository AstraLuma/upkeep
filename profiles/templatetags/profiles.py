from django import template

register = template.Library()

@register.simple_tag
def socialname(name):
    return {
    	'google-oauth2': 'Google',
    	'twitter': 'Twitter',
    	'facebook': 'Facebook',
    }[name]


