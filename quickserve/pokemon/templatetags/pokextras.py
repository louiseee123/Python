from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def type_to_number(type_name):
    """Map Pokemon type names to their corresponding number (1-18)"""
    type_map = {
        'normal': 1,
        'fighting': 2,
        'flying': 3,
        'poison': 4,
        'ground': 5,
        'rock': 6,
        'bug': 7,
        'ghost': 8,
        'steel': 9,
        'fire': 10,
        'water': 11,
        'grass': 12,
        'electric': 13,
        'psychic': 14,
        'ice': 15,
        'dragon': 16,
        'dark': 17,
        'fairy': 18,
    }
    return type_map.get(type_name.lower(), 1)
