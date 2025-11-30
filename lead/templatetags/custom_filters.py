from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    """מאפשר לגשת לפריט במילון לפי מפתח"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
