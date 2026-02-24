# Make pokedex Pokemon cards clickable to view detail

with open('pokemon/templates/pokemon/pokedex.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update pokemon card to be clickable
old_card = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-card rarity-{{ pokemon.rarity|lower }}">
                    <div class="pokemon-image">🐾{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">SHINY</span>{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">⭐</span>{% endif %}</div>
                    <span class="type-badge type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}-badge">{{ pokemon.rarity }}</span>
                </div>
                {% endif %}'''

new_card = '''                {% if pokemon.id in unlocked_ids %}
                <a href="{% url 'pokemon:pokemon_detail' pokemon.id %}" class="pokemon-card-link">
                    <div class="pokemon-card rarity-{{ pokemon.rarity|lower }}">
                        <div class="pokemon-image">🐾{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">SHINY</span>{% endif %}</div>
                        <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">⭐</span>{% endif %}</div>
                        <span class="type-badge type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                        <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}-badge">{{ pokemon.rarity }}</span>
                    </div>
                </a>
                {% endif %}'''

content = content.replace(old_card, new_card)

# Also update locked Pokemon to show locked message
old_locked = '''                {% if pokemon.id not in unlocked_ids %}
                <div class="pokemon-card locked">
                    <div class="pokemon-image">🔒</div>
                    <div class="pokemon-name">???</div>
                    <span class="type-badge">???</span>
                </div>
                {% endif %}'''

new_locked = '''                {% if pokemon.id not in unlocked_ids %}
                <a href="{% url 'pokemon:pokemon_detail' pokemon.id %}" class="pokemon-card-link">
                    <div class="pokemon-card locked">
                        <div class="pokemon-image">🔒</div>
                        <div class="pokemon-name">???</div>
                        <span class="type-badge">???</span>
                    </div>
                </a>
                {% endif %}'''

content = content.replace(old_locked, new_locked)

# Add CSS for card link
old_css = '''        .pokemon-card.locked {
            opacity: 0.5;
            cursor: not-allowed;
        }
    </style>'''

new_css = '''        .pokemon-card.locked {
            opacity: 0.5;
            cursor: not-allowed;
        }
        
        a.pokemon-card-link {
            text-decoration: none;
            color: inherit;
            display: inline-block;
        }
        
        a.pokemon-card-link:hover .pokemon-card {
            transform: scale(1.05);
            transition: transform 0.3s ease;
        }
    </style>'''

content = content.replace(old_css, new_css)

with open('pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Pokedex template updated - cards are now clickable!')
