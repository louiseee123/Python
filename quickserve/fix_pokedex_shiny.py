# Fix pokedex template with correct shiny syntax

with open('pokemon/templates/pokemon/pokedex.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-image">🐾{% if unlocked_data.pokemon.id == True %} ⭐{% endif %}</div>
                <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data.pokemon.id == True %} ⭐{% endif %}</div>'''

new = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-image">🐾{% if unlocked_data|get_item:pokemon.id %} ⭐{% endif %}</div>
                <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data|get_item:pokemon.id %} ⭐{% endif %}</div>'''

content = content.replace(old, new)

# Add the template tag at the top
old_top = '{% load static %}'
new_top = '''{% load static %}
{% load pokextras %}'''

content = content.replace(old_top, new_top)

with open('pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Create the templatetags directory and file
import os
templatetags_dir = 'pokemon/templatetags'
os.makedirs(templatetags_dir, exist_ok=True)

with open(f'{templatetags_dir}/__init__.py', 'w') as f:
    f.write('')

with open(f'{templatetags_dir}/pokextras.py', 'w') as f:
    f.write('''from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
''')

print('Pokedex template fixed')
