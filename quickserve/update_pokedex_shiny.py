# Update pokedex view to include shiny info

with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    # Get all unlocked Pokemon IDs
    unlocked_ids = trainer.unlocks.values_list('pokemon_id', flat=True)'''

new = '''    # Get all unlocked Pokemon IDs and their shiny status
    unlocked_data = {}  # {pokemon_id: is_shiny}
    for unlock in trainer.unlocks.all():
        unlocked_data[unlock.pokemon_id] = unlock.shiny'''

content = content.replace(old, new)

old2 = '''    context = {
        'pokemon_list': pokemon_list,
        'unlocked_ids': set(unlocked_ids),
        'types': types,
        'selected_type': pokemon_type,
        'search_query': search_query,
        'trainer': trainer,
    }'''

new2 = '''    context = {
        'pokemon_list': pokemon_list,
        'unlocked_ids': set(unlocked_data.keys()),
        'unlocked_data': unlocked_data,
        'types': types,
        'selected_type': pokemon_type,
        'search_query': search_query,
        'trainer': trainer,
    }'''

content = content.replace(old2, new2)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Pokedex view updated')

# Now update the template to show shiny stars
with open('pokemon/templates/pokemon/pokedex.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_template = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-image">🐾</div>
                <div class="pokemon-name">{{ pokemon.name }}</div>'''

new_template = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-image">🐾{% if unlocked_data.pokemon.id == True %} ⭐{% endif %}</div>
                <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data.pokemon.id == True %} ⭐{% endif %}</div>'''

content = content.replace(old_template, new_template)

with open('pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Pokedex template updated')
