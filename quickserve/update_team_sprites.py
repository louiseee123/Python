# Update my_team.html to use sprite images

team_content = '''{% load static %}
{% load pokextras %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Team - Pokémon Trainer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: white;
        }
        .navbar {
            background: rgba(0, 0, 0, 0.3);
            padding: 15px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-brand { font-size: 1.5rem; font-weight: bold; }
        .nav-links { display: flex; gap: 20px; }
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 8px 15px;
            border-radius: 20px;
            transition: all 0.3s ease;
        }
        .nav-links a:hover { background: rgba(255, 255, 255, 0.1); }
        .container { max-width: 1200px; margin: 0 auto; padding: 30px; }
        h1 { text-align: center; margin-bottom: 30px; font-size: 2rem; }
        
        a.team-member-link { text-decoration: none; color: inherit; }
        
        .team-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
            margin-bottom: 40px;
        }
        .team-member-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            min-width: 180px;
            max-width: 220px;
            flex: 1 1 180px;
        }
        .team-member-card:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.15);
        }
        /* Rarity borders */
        .team-member-card.rarity-common { border: 2px solid #a0a0a0; }
        .team-member-card.rarity-uncommon { border: 2px solid #4cd137; }
        .team-member-card.rarity-rare { border: 2px solid #00a8ff; }
        .team-member-card.rarity-epic { border: 2px solid #9c88ff; }
        .team-member-card.rarity-legendary {
            border: 3px solid #ffd700;
            animation: legendary-glow 2s ease-in-out infinite;
        }
        @keyframes legendary-glow {
            0%, 100% { box-shadow: 0 0 10px #ffd700, 0 0 20px #ffa502; }
            50% { box-shadow: 0 0 20px #ffd700, 0 0 40px #ffa502; }
        }
        
        .member-icon {
            width: 80px;
            height: 80px;
            margin: 0 auto 8px;
            object-fit: contain;
        }
        .shiny-star { color: #ffd700; text-shadow: 0 0 10px #ffd700; }
        .team-member-card h3 { margin-bottom: 5px; font-size: 1.1rem; word-wrap: break-word; }
        .member-type {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.75rem;
            font-weight: bold;
            margin-bottom: 8px;
        }
        .type-fire { background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
        .type-water { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
        .type-grass { background: linear-gradient(135deg, #95e881, #44a08d); }
        .type-electric { background: linear-gradient(135deg, #ffd93d, #f39c12); }
        .type-psychic { background: linear-gradient(135deg, #dda0dd, #8e44ad); }
        .type-ghost { background: linear-gradient(135deg, #7f8c8d, #2c3e50); }
        .type-dragon { background: linear-gradient(135deg, #3498db, #1a5276); }
        .type-normal { background: linear-gradient(135deg, #95a5a6, #7f8c8d); }
        
        .rarity-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.7rem;
            font-weight: bold;
            margin-top: 5px;
        }
        .rarity-common-badge { background: #6c757d; }
        .rarity-uncommon-badge { background: #28a745; }
        .rarity-rare-badge { background: #007bff; }
        .rarity-epic-badge { background: #6f42c1; }
        .rarity-legendary-badge { background: linear-gradient(45deg, #ffd700, #ff8c00); color: #000; }
        
        .member-actions {
            margin-top: 12px;
            display: flex;
            gap: 8px;
            justify-content: center;
            flex-wrap: wrap;
        }
        .btn {
            padding: 6px 12px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            text-decoration: none;
            font-weight: bold;
            font-size: 0.75rem;
            transition: all 0.3s ease;
        }
        .btn-primary { background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; }
        .btn-danger { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; }
        .btn:hover { transform: scale(1.05); }
        
        .empty-team {
            text-align: center;
            padding: 50px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
        }
        .empty-team p { margin-bottom: 20px; opacity: 0.7; }
        
        .click-hint { font-size: 0.65rem; opacity: 0.5; margin-top: 8px; }
        
        .available-pokemon { margin-top: 40px; }
        .available-pokemon h2 { margin-bottom: 20px; font-size: 1.5rem; }
        .available-pokemon > p { margin-bottom: 15px; opacity: 0.7; }
        
        .pokemon-grid { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 15px; 
            justify-content: center;
        }
        .pokemon-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            min-width: 140px;
            max-width: 160px;
            flex: 1 1 140px;
            transition: all 0.3s ease;
        }
        .pokemon-card:hover { 
            background: rgba(255, 255, 255, 0.15); 
            transform: translateY(-3px);
        }
        .pokemon-card .member-icon { width: 60px; height: 60px; }
        .pokemon-card h4 { font-size: 0.95rem; margin: 8px 0; word-wrap: break-word; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">⚔️ Pokemon Trainer</div>
        <div class="nav-links">
            <a href="{% url 'pokemon:dashboard' %}">Dashboard</a>
            <a href="{% url 'pokemon:pokedex' %}">Pokédex</a>
            <a href="{% url 'pokemon:my_team' %}" class="active">My Team</a>
            <a href="{% url 'pokemon:profile' %}">Profile</a>
            <a href="{% url 'pokemon:logout' %}">Logout</a>
        </div>
    </nav>
    
    <div class="container">
        <h1>👥 My Team</h1>
        
        {% if members %}
        <div class="team-grid">
            {% for member in members %}
            <a href="{% url 'pokemon:pokemon_detail' member.pokemon.id %}" class="team-member-link">
                <div class="team-member-card rarity-{{ member.pokemon.rarity|lower }}">
                    <img src="{{ member.pokemon.sprite_url }}" alt="{{ member.pokemon.name }}" class="member-icon">
                    <h3>{{ member.nickname|default:member.pokemon.name }}{% if team_shiny|get_item:member.id %} ⭐{% endif %}</h3>
                    <p class="member-type type-{{ member.pokemon.type|lower }}">{{ member.pokemon.type }}</p>
                    <span class="rarity-badge rarity-{{ member.pokemon.rarity|lower }}-badge">{{ member.pokemon.rarity }}</span>
                    <div class="member-actions" onclick="event.preventDefault(); event.stopPropagation();">
                        <a href="{% url 'pokemon:rename_member' member.id %}" class="btn btn-primary">Rename</a>
                        <a href="{% url 'pokemon:remove_from_team' member.id %}" class="btn btn-danger">Remove</a>
                    </div>
                    <p class="click-hint">Click for details</p>
                </div>
            </a>
            {% endfor %}
        </div>
        {% else %}
        <div class="empty-team">
            <p>Your team is empty!</p>
            <a href="{% url 'pokemon:pokedex' %}" class="btn btn-primary">Go to Pokédex</a>
        </div>
        {% endif %}
        
        <div class="available-pokemon">
            <h2>📦 Available Pokemon</h2>
            <p>Click to add to your team</p>
            <div class="pokemon-grid">
                {% for p in available_pokemon %}
                <a href="{% url 'pokemon:pokemon_detail' p.0.id %}" class="team-member-link">
                    <div class="pokemon-card">
                        <img src="{{ p.0.sprite_url }}" alt="{{ p.0.name }}" class="member-icon">
                        <h4>{{ p.0.name }}{% if p.1 %} ⭐{% endif %}</h4>
                        <span class="member-type type-{{ p.0.type|lower }}">{{ p.0.type }}</span>
                    </div>
                </a>
                {% endfor %}
            </div>
        </div>
    </div>
</body>
</html>
'''

with open('quickserve/pokemon/templates/pokemon/my_team.html', 'w', encoding='utf-8') as f:
    f.write(team_content)

print('Updated my_team.html with sprite images!')
