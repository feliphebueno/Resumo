'''
Created on Feb 17, 2017

@author: root
'''
from django import template
from django.template.defaultfilters import stringfilter
import json


register = template.Library()

@register.filter(name='replace')
@stringfilter
def replace(value, arg):
    options = json.loads(arg)
    if(value in options):
        return options[value]
    else:
        return None

@register.filter(name='keys')
def keys(value, arg):
    print("VAL: > "+ json.dumps(value))
    print("ARG: > "+ json.dumps(arg))

    """Removes all values of arg from the given string"""
    return None

register.filter('replace', replace)
register.filter('keys', keys)
