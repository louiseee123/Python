# Make my_team Pokemon cards clickable to view detail

with open('pokemon/templates/pokemon/my_team.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update team member card to be clickable
old_card = '''            {% for member in team_members %}
            <div class="team-member-card rarity-{{ member.pokemon.rarity|lower }}">
                <div class="member-icon">
                    🐾{% if member.shiny %}<span class="shiny-star">⭐</span>{% endif %}
                </div>
                <h3>{{ member.nickname|default:member.pokemon.name }}{% if member.shiny %}<span class="shiny-star">⭐</span>{% endif %}</h3>
                <p class="member-type">{{ member.pokemon.type }}</p>
                <span class="rarity-badge rarity-{{ member.pokemon.rarity|lower }}-badge">{{ member.pokemon.rarity }}</span>
                <div class="member-actions">
                    <a href="{% url 'pokemon:rename_member' member.id %}" class="btn btn-small">Rename</a>
                    <a href="{% url 'pokemon:remove_from_team' member.id %}" class="btn btn-small btn-danger">Remove</a>
                </div>
            </div>
            {% endfor %}'''

new_card = '''            {% for member in team_members %}
            <a href="{% url 'pokemon:pokemon_detail' member.pokemon.id %}" class="team-member-link">
                <div class="team-member-card rarity-{{ member.pokemon.rarity|lower }}">
                    <div class="member-icon">
                        🐾{% if member.shiny %}<span class="shiny-star">⭐</span>{% endif %}
                    </div>
                    <h3>{{ member.nickname|default:member.pokemon.name }}{% if member.shiny %}<span class="shiny-star">⭐</span>{% endif %}</h3>
                    <p class="member-type">{{ member.pokemon.type }}</p>
                    <span class="rarity-badge rarity-{{ member.pokemon.rarity|lower }}-badge">{{ member.pokemon.rarity }}</span>
                    <div class="member-actions" onclick="event.preventDefault(); event.stopPropagation();">
                        <a href="{% url 'pokemon:rename_member' member.id %}" class="btn btn-small">Rename</a>
                        <a href="{% url 'pokemon:remove_from_team' member.id %}" class="btn btn-small btn-danger">Remove</a>
                    </div>
                </div>
            </a>
            {% endfor %}'''

content = content.replace(old_card, new_card)

# Add CSS for team member link
old_css = '''        .team-member-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .team-member-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }'''

new_css = '''        .team-member-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .team-member-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        
        a.team-member-link {
            text-decoration: none;
            color: inherit;
            display: inline-block;
        }'''

content = content.replace(old_css, new_css)

with open('pokemon/templates/pokemon/my_team.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('My Team template updated - cards are now clickable!')
