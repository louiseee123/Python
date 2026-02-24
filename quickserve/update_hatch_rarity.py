# Update hatch_result template to add legendary glow effect

with open('pokemon/templates/pokemon/hatch_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add legendary glow CSS
old_css = '''        .rarity-legendary { background: linear-gradient(135deg, #f1c40f, #f39c12); color: #1a1a2e; }

        .added-to-team {'''

new_css = '''        .rarity-legendary { 
            background: linear-gradient(135deg, #f1c40f, #f39c12); 
            color: #1a1a2e; 
            animation: legendary-glow 2s ease-in-out infinite;
        }

        @keyframes legendary-glow {
            0%, 100% { 
                box-shadow: 0 0 20px #ffd700, 0 0 40px #ffa502, 0 0 60px #ff7f50;
            }
            50% { 
                box-shadow: 0 0 30px #ffd700, 0 0 60px #ffa502, 0 0 90px #ff7f50;
            }
        }

        .pokemon-card.legendary {
            border-color: #ffd700;
            animation: legendary-glow 2s ease-in-out infinite;
        }

        .added-to-team {'''

content = content.replace(old_css, new_css)

# Update pokemon-card div to include legendary class
old_card = '''        <div class="pokemon-card">
            <div class="pokemon-image">🐾{% if is_shiny %} ⭐{% endif %}</div>'''

new_card = '''        <div class="pokemon-card{% if rarity == 'Legendary' %} legendary{% endif %}">
            <div class="pokemon-image">🐾{% if is_shiny %} ⭐{% endif %}</div>'''

content = content.replace(old_card, new_card)

with open('pokemon/templates/pokemon/hatch_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

