# This script updates the hatch_result.html template

old_content = '''            <div class="xp-badge">+10 XP</div>
            
            {% if added_to_team %}
            <div class="added-to-team">✓ Added to your team!</div>
            {% else %}
            <div style="margin-top: 10px; opacity: 0.7; font-size: 0.9rem;">
                Team is full - add from Pokédex
            </div>
            {% endif %}'''

new_content = '''            <div class="rarity-badge" style="background: linear-gradient(135deg, #{{rarity_color}}, #{{rarity_color_dark}}); padding: 8px 16px; border-radius: 15px; margin-bottom: 15px; font-weight: bold;">
                {{ rarity }}
            </div>
            
            <div class="xp-badge">+{{ xp_earned }} XP</div>
            
            {% if added_to_team %}
            <div class="added-to-team">✓ Added to your team!</div>
            {% elif duplicate_pokemon %}
            <div style="margin-top: 10px; color: #f39c12; font-size: 0.9rem;">
                Already in team - found in Pokédex!
            </div>
            {% else %}
            <div style="margin-top: 10px; opacity: 0.7; font-size: 0.9rem;">
                Team is full - add from Pokédex
            </div>
            {% endif %}
            
            {% if already_unlocked and not added_to_team %}
            <div style="margin-top: 5px; opacity: 0.7; font-size: 0.85rem;">
                (You already had this Pokemon)
            </div>
            {% endif %}'''

with open('pokemon/templates/pokemon/hatch_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(old_content, new_content)

with open('pokemon/templates/pokemon/hatch_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done updating hatch_result.html template')
