# Fix pokedex.html - remove description from cards

content = '''{% load static %}
{% load pokextras %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pokédex - Pokémon Trainer</title>
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
        .filters { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px; }
        .filter-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .filter-btn:hover, .filter-btn.active { background: linear-gradient(135deg, #ff6b6b, #4ecdc4); }
        .search-box { display: flex; justify-content: center; margin-bottom: 30px; }
        .search-box input {
            padding: 12px 20px;
            border: none;
            border-radius: 50px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 1rem;
            width: 300px;
        }
        .search-box input::placeholder { color: rgba(255, 255, 255, 0.5); }
        
        .pokemon-grid { 
            display: flex; 
            flex-wrap: wrap; 
            gap: 15px; 
            justify-content: center;
        }
        
        a.pokemon-card-link { text-decoration: none; color: inherit; }
        
        .pokemon-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            min-width: 140px;
            max-width: 160px;
            flex: 1 1 140px;
        }
        .pokemon-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.15); }
        .pokemon-card.locked { opacity: 0.5; filter: grayscale(100%); }
        .pokemon-card.locked:hover { transform: none; }
        
        .pokemon-image {
            width: 70px; height: 70px;
            margin: 0 auto 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 2rem;
        }
        .pokemon-name { font-size: 0.95rem; font-weight: bold; margin-bottom: 8px; }
        .pokemon-type {
            display: inline-block; padding: 4px 10px;
            border-radius: 12px; font-size: 0.7rem; font-weight: bold;
        }
        .type-fire { background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
        .type-water { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
        .type-grass { background: linear-gradient(135deg, #95e881, #44a08d); }
        .type-electric { background: linear-gradient(135deg, #ffd93d, #f39c12); }
        .type-psychic { background: linear-gradient(135deg, #dda0dd, #8e44ad); }
        .type-ghost { background: linear-gradient(135deg, #7f8c8d, #2c3e50); }
        .type-dragon { background: linear-gradient(135deg, #3498db, #1a5276); }
        .type-normal { background: linear-gradient(135deg, #95a5a6, #7f8c8d); }
        
        .level-req { font-size: 0.75rem; margin-top: 5px; }
        
        .rarity-badge {
            display: inline-block;
            padding: 2px 8px;
            border-radius: 8px;
            font-size: 0.65rem;
            font-weight: bold;
            margin-top: 5px;
        }
        .rarity-common { background: #6c757d; }
        .rarity-uncommon { background: #28a745; }
        .rarity-rare { background: #007bff; }
        .rarity-epic { background: #6f42c1; }
        .rarity-legendary { background: linear-gradient(45deg, #ffd700, #f39c12); color: #1a1a2e; }
        
        .lock-icon { font-size: 1.5rem; margin-bottom: 10px; }
        
        .btn {
            display: inline-block; padding: 6px 12px;
            border: none; border-radius: 12px;
            cursor: pointer; text-decoration: none;
            font-weight: bold; font-size: 0.7rem; margin-top: 8px;
        }
        .btn-primary { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; }
        .btn-primary:hover { transform: scale(1.05); }
        
        .click-hint { font-size: 0.6rem; opacity: 0.5; margin-top: 6px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">⚔️ Pokemon Trainer</div>
        <div class="nav-links">
            <a href="{% url 'pokemon:dashboard' %}">Dashboard</a>
            <a href="{% url 'pokemon:pokedex' %}" class="active">Pokédex</a>
            <a href="{% url 'pokemon:my_team' %}">My Team</a>
            <a href="{% url 'pokemon:profile' %}">Profile</a>
            <a href="{% url 'pokemon:logout' %}">Logout</a>
        </div>
    </nav>
    
    <div class="container">
        <h1>📚 Pokédex</h1>
        
        <div class="filters">
            <a href="{% url 'pokemon:pokedex' %}" class="filter-btn {% if not selected_type %}active{% endif %}">All</a>
            {% for type_code, type_name in types %}
            <a href="?type={{ type_code }}" class="filter-btn {% if selected_type == type_code %}active{% endif %}">{{ type_name }}</a>
            {% endfor %}
        </div>
        
        <div class="search-box">
            <form method="get">
                {% if selected_type %}
                <input type="hidden" name="type" value="{{ selected_type }}">
                {% endif %}
                <input type="text" name="search" placeholder="Search Pokemon..." value="{{ search_query }}">
            </form>
        </div>
        
        <div class="pokemon-grid">
            {% for pokemon in pokemon_list %}
            <a href="{% url 'pokemon:pokemon_detail' pokemon.id %}" class="pokemon-card-link">
                <div class="pokemon-card {% if pokemon.id not in unlocked_ids %}locked{% endif %}">
                    {% if pokemon.id in unlocked_ids %}
                    <div class="pokemon-image">🐾</div>
                    <div class="pokemon-name">{{ pokemon.name }}</div>
                    <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <p class="level-req"><span class="rarity-badge rarity-{{ pokemon.rarity|lower }}">{{ pokemon.rarity }}</span></p>
                    {% if not pokemon.id in team_pokemon_ids %}
                    <span class="btn btn-primary" onclick="event.preventDefault(); event.stopPropagation(); window.location.href='{% url 'pokemon:add_to_team' pokemon.id %}'">Add</span>
                    {% endif %}
                    {% else %}
                    <div class="lock-icon">🔒</div>
                    <div class="pokemon-name">{{ pokemon.name }}</div>
                    <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <p class="level-req"><span class="rarity-badge rarity-{{ pokemon.rarity|lower }}">{{ pokemon.rarity }}</span></p>
                    {% endif %}
                    <p class="click-hint">Click for details</p>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

with open('quickserve/pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('pokedex.html fixed - description removed from cards!')
