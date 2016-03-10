from django import template

register = template.Library()

@register.simple_tag
def socialname(name):
    """Removes all values of arg from the given string"""
    return {
    	'google-oauth2': 'Google',
    	'twitter': 'Twitter',
    	'facebook': 'Facebook',
    }[name]


