# Fix pokedex.html to make cards clickable

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
        h1 { text-align: center; margin-bottom: 30px; font-size: 2.5rem; }
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
        .pokemon-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 20px; }
        
        a.pokemon-card-link { text-decoration: none; color: inherit; display: block; }
        
        .pokemon-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        .pokemon-card:hover { transform: translateY(-5px); background: rgba(255, 255, 255, 0.15); }
        .pokemon-card.locked { opacity: 0.5; filter: grayscale(100%); }
        .pokemon-card.locked:hover { transform: none; }
        
        .pokemon-image {
            width: 100px; height: 100px;
            margin: 0 auto 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 3rem;
        }
        .pokemon-name { font-size: 1.2rem; font-weight: bold; margin-bottom: 10px; }
        .pokemon-type {
            display: inline-block; padding: 5px 15px;
            border-radius: 20px; font-size: 0.8rem; font-weight: bold; margin-bottom: 10px;
        }
        .type-fire { background: linear-gradient(135deg, #ff6b6b, #ee5a24); }
        .type-water { background: linear-gradient(135deg, #4ecdc4, #44a08d); }
        .type-grass { background: linear-gradient(135deg, #95e881, #44a08d); }
        .type-electric { background: linear-gradient(135deg, #ffd93d, #f39c12); }
        .type-psychic { background: linear-gradient(135deg, #dda0dd, #8e44ad); }
        .type-ghost { background: linear-gradient(135deg, #7f8c8d, #2c3e50); }
        .type-dragon { background: linear-gradient(135deg, #3498db, #1a5276); }
        .type-normal { background: linear-gradient(135deg, #95a5a6, #7f8c8d); }
        
        .level-req { font-size: 0.9rem; opacity: 0.7; }
        
        .rarity-common { background: linear-gradient(135deg, #95a5a6, #7f8c8d); }
        .rarity-uncommon { background: linear-gradient(135deg, #2ecc71, #27ae60); }
        .rarity-rare { background: linear-gradient(135deg, #3498db, #2980b9); }
        .rarity-epic { background: linear-gradient(135deg, #9b59b6, #8e44ad); }
        .rarity-legendary { background: linear-gradient(135deg, #f1c40f, #f39c12); color: #1a1a2e; }
        
        .lock-icon { font-size: 2rem; margin-top: 20px; }
        
        .btn {
            display: inline-block; padding: 8px 16px;
            border: none; border-radius: 20px;
            cursor: pointer; text-decoration: none;
            font-weight: bold; transition: all 0.3s ease; margin-top: 10px;
        }
        .btn-primary { background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; }
        .btn-primary:hover { transform: scale(1.05); }
        .pokemon-description { font-size: 0.8rem; opacity: 0.7; margin-top: 10px; line-height: 1.4; }
        
        .click-hint { font-size: 0.7rem; opacity: 0.5; margin-top: 8px; }
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
                    <div class="pokemon-image">🐾{% if unlocked_data|get_item:pokemon.id %} ⭐{% endif %}</div>
                    <div class="pokemon-name">{{ pokemon.name }}{% if unlocked_data|get_item:pokemon.id %} ⭐{% endif %}</div>
                    <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <p class="level-req" style="color: #ffd93d; margin-top: 5px;">{{ pokemon.get_rarity_display }}</p>
                    <p class="pokemon-description">{{ pokemon.description }}</p>
                    {% if not pokemon.id in team_pokemon_ids %}
                    <span class="btn btn-primary" onclick="event.preventDefault(); event.stopPropagation(); window.location.href='{% url 'pokemon:add_to_team' pokemon.id %}'">Add to Team</span>
                    {% endif %}
                    {% else %}
                    <div class="lock-icon">🔒</div>
                    <div class="pokemon-name">{{ pokemon.name }}</div>
                    <span class="pokemon-type type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <p class="level-req">{{ pokemon.get_rarity_display }}</p>
                    {% endif %}
                    <p class="click-hint">Click to view details</p>
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

print('pokedex.html fixed - cards are now clickable!')
