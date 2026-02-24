# Update my_team view to include shiny info

with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and update the my_team view to get shiny info
old = '''    # Get unlocked Pokemon that are not in team
    unlocked_pokemon = trainer.unlocks.select_related('pokemon')
    team_pokemon_ids = team.members.values_list('pokemon_id', flat=True)
    available_pokemon = [u.pokemon for u in unlocked_pokemon if u.pokemon.id not in team_pokemon_ids]'''

new = '''    # Get unlocked Pokemon that are not in team (with shiny status)
    unlocked_pokemon = trainer.unlocks.select_related('pokemon')
    team_pokemon_ids = team.members.values_list('pokemon_id', flat=True)
    available_pokemon = []  # List of (pokemon, shiny) tuples
    for u in unlocked_pokemon:
        if u.pokemon.id not in team_pokemon_ids:
            available_pokemon.append((u.pokemon, u.shiny))'''

content = content.replace(old, new)

# Update the context
old2 = '''    context = {
        'trainer': trainer,
        'team': team,
        'members': members,
        'available_pokemon': available_pokemon,
    }'''

new2 = '''    # Get shiny status for team members
    team_shiny = {}  # {member_id: is_shiny}
    for member in members:
        unlock = trainer.unlocks.filter(pokemon=member.pokemon).first()
        team_shiny[member.id] = unlock.shiny if unlock else False
    
    context = {
        'trainer': trainer,
        'team': team,
        'members': members,
        'team_shiny': team_shiny,
        'available_pokemon': available_pokemon,
    }'''

content = content.replace(old2, new2)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('my_team view updated')

# Now update the my_team template to show shiny stars
with open('pokemon/templates/pokemon/my_team.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update team member display
old_t = '''                <div class="team-member">
                    <div class="member-image">🐾</div>
                    <div class="member-name">{{ member.nickname|default:member.pokemon.name }}</div>'''

new_t = '''                <div class="team-member">
                    <div class="member-image">🐾{% if team_shiny|get_item:member.id %} ⭐{% endif %}</div>
                    <div class="member-name">{{ member.nickname|default:member.pokemon.name }}{% if team_shiny|get_item:member.id %} ⭐{% endif %}</div>'''

content = content.replace(old_t, new_t)

# Update available pokemon display
old_a = '''                <div class="pokemon-card">
                    <div class="pokemon-image">🐾</div>
                    <div class="pokemon-name">{{ pokemon.name }}</div>'''

new_a = '''                <div class="pokemon-card">
                    <div class="pokemon-image">🐾{% if shiny %} ⭐{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if shiny %} ⭐{% endif %}</div>'''

content = content.replace(old_a, new_a)

# Update the for loop to unpack the tuple
old_loop = '''{% for pokemon in available_pokemon %}'''
new_loop = '''{% for pokemon, shiny in available_pokemon %}'''

content = content.replace(old_loop, new_loop)

with open('pokemon/templates/pokemon/my_team.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('my_team template updated')
