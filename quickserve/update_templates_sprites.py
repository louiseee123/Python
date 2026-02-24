# Update templates to use sprite images

# Update pokedex.html
pokedex_content = '''{% load static %}
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
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 15px; 
        }
        
        a.pokemon-card-link { text-decoration: none; color: inherit; display: block; }
        
        .pokemon-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: space-between;
            min-height: 180px;
        }
        .pokemon-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.15); }
        .pokemon-card.locked { opacity: 0.5; filter: grayscale(100%); }
        .pokemon-card.locked:hover { transform: none; }
        
        .pokemon-image {
            width: 80px; height: 80px;
            margin: 0 auto 8px;
            object-fit: contain;
            flex-shrink: 0;
        }
        .pokemon-name { font-size: 0.9rem; font-weight: bold; margin-bottom: 4px; }
        .pokemon-type {
            display: inline-block; padding: 3px 8px;
            border-radius: 10px; font-size: 0.65rem; font-weight: bold;
            flex-shrink: 0;
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
            padding: 2px 6px;
            border-radius: 6px;
            font-size: 0.6rem;
            font-weight: bold;
            margin-top: 4px;
            flex-shrink: 0;
        }
        .rarity-common { background: #6c757d; }
        .rarity-uncommon { background: #28a745; }
        .rarity-rare { background: #007bff; }
        .rarity-epic { background: #6f42c1; }
        .rarity-legendary { background: linear-gradient(45deg, #ffd700, #f39c12); color: #1a1a2e; }
        
        .lock-icon { font-size: 1.5rem; margin-bottom: 8px; flex-shrink: 0; }
        
        .btn {
            display: inline-block; padding: 5px 10px;
            border: none; border-radius: 10px;
            cursor: pointer; text-decoration: none;
            font-weight: bold; font-size: 0.65rem; margin-top: 6px;
            flex-shrink: 0;
        }
        .btn-primary { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; }
        .btn-primary:hover { transform: scale(1.05); }
        
        .click-hint { font-size: 0.55rem; opacity: 0.5; margin-top: 6px; flex-shrink: 0; }
        
        .card-content { display: flex; flex-direction: column; align-items: center; width: 100%; }
        .card-actions { margin-top: auto; }
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
                    <div class="card-content">
                        {% if pokemon.id in unlocked_ids %}
                        <img src="{{ pokemon.sprite_url }}" alt="{{ pokemon.name }}" class="pokemon-image">
                        <div class="pokemon-name">{{ pokemon.name }}</div>
                        <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                        <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}">{{ pokemon.rarity }}</span>
                        {% else %}
                        <div class="lock-icon">🔒</div>
                        <div class="pokemon-name">{{ pokemon.name }}</div>
                        <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                        <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}">{{ pokemon.rarity }}</span>
                        {% endif %}
                    </div>
                    <div class="card-actions">
                        {% if pokemon.id in unlocked_ids and not pokemon.id in team_pokemon_ids %}
                        <span class="btn btn-primary" onclick="event.preventDefault(); event.stopPropagation(); window.location.href='{% url 'pokemon:add_to_team' pokemon.id %}'">Add</span>
                        {% endif %}
                        <p class="click-hint">Click for details</p>
                    </div>
                </div>
            </a>
            {% endfor %}
        </div>
    </div>
</body>
</html>
'''

with open('quickserve/pokemon/templates/pokemon/pokedex.html', 'w', encoding='utf-8') as f:
    f.write(pokedex_content)

print('Updated pokedex.html with sprite images!')
