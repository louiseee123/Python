# Update pokedex template to show rarity

with open('pokemon/templates/pokemon/pokedex.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS for rarity styles in pokedex
old_styles = '''        .shiny-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            color: #000;
        }
    </style>'''

new_styles = '''        .shiny-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            color: #000;
        }
        
        /* Rarity glow effects */
        .pokemon-card.rarity-legendary { 
            border: 3px solid #ffd700;
            animation: legendary-glow 2s ease-in-out infinite;
        }
        
        @keyframes legendary-glow {
            0%, 100% { 
                box-shadow: 0 0 10px #ffd700, 0 0 20px #ffa502;
            }
            50% { 
                box-shadow: 0 0 20px #ffd700, 0 0 40px #ffa502;
            }
        }
        
        .rarity-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-left: 5px;
        }
        .rarity-common-badge { background: #6c757d; }
        .rarity-uncommon-badge { background: #28a745; }
        .rarity-rare-badge { background: #007bff; }
        .rarity-epic-badge { background: #6f42c1; color: white; }
        .rarity-legendary-badge { background: linear-gradient(45deg, #ffd700, #ff8c00); color: #000; }
        
        .rarity-common { border: 2px solid #6c757d; }
        .rarity-uncommon { border: 2px solid #28a745; }
        .rarity-rare { border: 2px solid #007bff; }
        .rarity-epic { border: 2px solid #6f42c1; }
    </style>'''

content = content.replace(old_styles, new_styles)

# Update pokemon card to include rarity
old_card = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-card">
                    <div class="pokemon-image">🐾{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">SHINY</span>{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">⭐</span>{% endif %}</div>
                    <span class="type-badge type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                </div>
                {% endif %}'''

new_card = '''                {% if pokemon.id in unlocked_ids %}
                <div class="pokemon-card rarity-{{ pokemon.rarity|lower }}">
                    <div class="pokemon-image">🐾{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">SHINY</span>{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data|get_item:pokemon.id %} <span class="shiny-badge">⭐</span>{% endif %}</div>
                    <span class="type-badge type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}-badge">{{ pokemon.rarity }}</span>
                </div>
                {% endif %}'''

content = content.replace(old_card, new_card)

with open('pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('pokedex template updated with rarity!')
