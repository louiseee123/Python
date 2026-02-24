# Update hatch_result.html to show shiny star

with open('pokemon/templates/pokemon/hatch_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        <div class="pokemon-card">
            <div class="pokemon-image">🐾</div>
            <div class="pokemon-name">{{ pokemon.name }}</div>
            <div class="pokemon-type">
                <span>{{ pokemon.type }}</span>
            </div>
            <div class="pokemon-desc">{{ pokemon.description }}</div>
            
            <div class="rarity-badge rarity-{{ rarity|lower }}">
                {{ rarity }}
            </div>
            
            <div class="xp-badge">+{{ xp_earned }} XP</div>
            
            <p style="margin-top: 15px; font-size: 1.1rem;">Rarity: <strong>{{ rarity }}</strong></p>'''

new = '''        <div class="pokemon-card">
            <div class="pokemon-image">🐾{% if is_shiny %} ⭐{% endif %}</div>
            <div class="pokemon-name">{{ pokemon.name }}{% if is_shiny %} ⭐{% endif %}</div>
            <div class="pokemon-type">
                <span>{{ pokemon.type }}</span>
            </div>
            <div class="pokemon-desc">{{ pokemon.description }}</div>
            
            {% if is_shiny %}
            <div class="rarity-badge" style="background: linear-gradient(135deg, #ff6b6b, #ee5a5a); color: white;">
                ⭐ SHINY ⭐
            </div>
            {% else %}
            <div class="rarity-badge rarity-{{ rarity|lower }}">
                {{ rarity }}
            </div>
            {% endif %}
            
            <div class="xp-badge">+{{ xp_earned }} XP</div>
            
            <p style="margin-top: 15px; font-size: 1.1rem;">Rarity: <strong>{{ rarity }}</strong></p>'''

content = content.replace(old, new)

with open('pokemon/templates/pokemon/hatch_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Hatch result template updated')
