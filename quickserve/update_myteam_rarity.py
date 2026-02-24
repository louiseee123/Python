# Update my_team template to show rarity with glowing borders for Legendary

with open('pokemon/templates/pokemon/my_team.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS for rarity glow effects - insert after the existing styles
old_styles = '''    .empty-state {
            text-align: center;
            padding: 40px;
            opacity: 0.7;
        }
    </style>'''

new_styles = '''    .empty-state {
            text-align: center;
            padding: 40px;
            opacity: 0.7;
        }
        
        /* Rarity glow effects */
        .rarity-common { border: 2px solid #a0a0a0; }
        .rarity-uncommon { border: 2px solid #4cd137; }
        .rarity-rare { border: 2px solid #00a8ff; }
        .rarity-epic { border: 2px solid #9c88ff; }
        .rarity-legendary { 
            border: 3px solid #ffd700;
            animation: legendary-glow 2s ease-in-out infinite;
        }
        
        @keyframes legendary-glow {
            0%, 100% { 
                box-shadow: 0 0 10px #ffd700, 0 0 20px #ffa502, 0 0 30px #ff7f50;
            }
            50% { 
                box-shadow: 0 0 20px #ffd700, 0 0 40px #ffa502, 0 0 60px #ff7f50;
            }
        }
        
        .rarity-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-top: 5px;
        }
        .rarity-common-badge { background: #6c757d; }
        .rarity-uncommon-badge { background: #28a745; }
        .rarity-rare-badge { background: #007bff; }
        .rarity-epic-badge { background: #6f42c1; }
        .rarity-legendary-badge { background: linear-gradient(45deg, #ffd700, #ff8c00); }
        
        .shiny-star {
            color: #ffd700;
            text-shadow: 0 0 5px #ffd700;
        }
    </style>'''

content = content.replace(old_styles, new_styles)

# Update team member to show rarity and glow
old_member = '''                <div class="team-member">
                    <div class="member-image">🐾{% if team_shiny|get_item:member.id %} ⭐{% endif %}</div>
                    <div class="member-name">{{ member.nickname|default:member.pokemon.name }}{% if team_shiny|get_item:member.id %} ⭐{% endif %}</div>
                    <span class="member-type type-{{ member.pokemon.type|lower }}">{{ member.pokemon.type }}</span>'''

new_member = '''                <div class="team-member rarity-{{ member.pokemon.rarity|lower }}">
                    <div class="member-image">🐾{% if team_shiny|get_item:member.id %} <span class="shiny-star">⭐</span>{% endif %}</div>
                    <div class="member-name">{{ member.nickname|default:member.pokemon.name }}{% if team_shiny|get_item:member.id %} <span class="shiny-star">⭐</span>{% endif %}</div>
                    <span class="member-type type-{{ member.pokemon.type|lower }}">{{ member.pokemon.type }}</span>
                    <span class="rarity-badge rarity-{{ member.pokemon.rarity|lower }}-badge">{{ member.pokemon.rarity }}</span>'''

content = content.replace(old_member, new_member)

# Update available pokemon to show rarity
old_available = '''                <div class="pokemon-card">
                    <div class="pokemon-image">🐾{% if shiny %} ⭐{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if shiny %} ⭐{% endif %}</div>
                    <span class="member-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>'''

new_available = '''                <div class="pokemon-card rarity-{{ pokemon.rarity|lower }}">
                    <div class="pokemon-image">🐾{% if shiny %} <span class="shiny-star">⭐</span>{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if shiny %} <span class="shiny-star">⭐</span>{% endif %}</div>
                    <span class="member-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}-badge">{{ pokemon.rarity }}</span>'''

content = content.replace(old_available, new_available)

with open('pokemon/templates/pokemon/my_team.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('my_team template updated with rarity and glowing borders!')
