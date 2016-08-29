from django import template

register = template.Library()

@register.filter
def index(sequence, position):
	return sequence[position]

@register.filter
def subtract(value, arg):
	return int(value) - int(arg)