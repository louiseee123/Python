# Update dashboard.html with rarity effects in team section

with open('pokemon/templates/pokemon/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add rarity CSS styles
old_css = '''        /* Hatch Animation */
        .hatch-anim {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 8rem;
            z-index: 1000;
            animation: hatch 2s ease forwards;
        }
        @keyframes hatch {
            0% { transform: translate(-50%, -50%) scale(0); }
            30% { transform: translate(-50%, -50%) scale(1.2); }
            50% { transform: translate(-50%, -50%) scale(1); }
            70% { transform: translate(-50%, -50%) rotate(360deg); }
            100% { transform: translate(-50%, -50%) scale(0); }
        }
    </style>'''

new_css = '''        /* Hatch Animation */
        .hatch-anim {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 8rem;
            z-index: 1000;
            animation: hatch 2s ease forwards;
        }
        @keyframes hatch {
            0% { transform: translate(-50%, -50%) scale(0); }
            30% { transform: translate(-50%, -50%) scale(1.2); }
            50% { transform: translate(-50%, -50%) scale(1); }
            70% { transform: translate(-50%, -50%) rotate(360deg); }
            100% { transform: translate(-50%, -50%) scale(0); }
        }
        
        /* Rarity effects */
        .team-member.rarity-common { border: 2px solid #a0a0a0; }
        .team-member.rarity-uncommon { border: 2px solid #4cd137; }
        .team-member.rarity-rare { border: 2px solid #00a8ff; }
        .team-member.rarity-epic { border: 2px solid #9c88ff; }
        .team-member.rarity-legendary { 
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
            padding: 2px 6px;
            border-radius: 8px;
            font-size: 0.65rem;
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

content = content.replace(old_css, new_css)

# Update team member to include rarity
old_team = '''            <div class="team-preview">
                {% for member in team_members %}
                <div class="team-member">
                    <div class="team-member-icon">🐾</div>
                    <div>{{ member.nickname|default:member.pokemon.name }}</div>
                    <small style="opacity: 0.7">{{ member.pokemon.type }}</small>
                </div>
                {% empty %}'''

new_team = '''            <div class="team-preview">
                {% for member in team_members %}
                <div class="team-member rarity-{{ member.pokemon.rarity|lower }}">
                    <div class="team-member-icon">🐾{% if member.shiny %} <span class="shiny-star">⭐</span>{% endif %}</div>
                    <div>{{ member.nickname|default:member.pokemon.name }}{% if member.shiny %} <span class="shiny-star">⭐</span>{% endif %}</div>
                    <small style="opacity: 0.7">{{ member.pokemon.type }}</small>
                    <span class="rarity-badge rarity-{{ member.pokemon.rarity|lower }}-badge">{{ member.pokemon.rarity }}</span>
                </div>
                {% empty %}'''

content = content.replace(old_team, new_team)

with open('pokemon/templates/pokemon/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('dashboard.html updated with rarity effects in team section!')
