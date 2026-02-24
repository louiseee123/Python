# Update pokedex.html to show rarity instead of level

with open('pokemon/templates/pokemon/pokedex.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''                <p class="level-req">Unlock at Level {{ pokemon.level_requirement }}</p>'''

new = '''                <p class="level-req">{{ pokemon.get_rarity_display }}</p>'''

content = content.replace(old, new)

# Also add rarity badge for unlocked Pokemon
old2 = '''                <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                <p class="pokemon-description">{{ pokemon.description }}</p>'''

new2 = '''                <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                <p class="level-req" style="color: #ffd93d; margin-top: 5px;">{{ pokemon.get_rarity_display }}</p>
                <p class="pokemon-description">{{ pokemon.description }}</p>'''

content = content.replace(old2, new2)

# Add rarity CSS
css_add = '''        
        .rarity-common { background: linear-gradient(135deg, #95a5a6, #7f8c8d); }
        .rarity-uncommon { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .rarity-rare { background: linear-gradient(135deg, #3498db, #2980b9); }
        .rarity-epic { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
        .rarity-legendary { background: linear-gradient(135deg, #f1c40f, #f39c12); color: #1a1a2e; }'''

# Add before .level-req
old3 = '''        .level-req {
            font-size: 0.9rem;
            opacity: 0.7;
        }'''

new3 = '''        .level-req {
            font-size: 0.9rem;
            opacity: 0.7;
        }
''' + css_add

content = content.replace(old3, new3)

with open('pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
