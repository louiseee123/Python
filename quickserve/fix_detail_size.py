# Fix pokemon_detail.html - make it smaller

content = '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ pokemon.name }} - Pokemon Details</title>
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
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .nav-brand { font-size: 1.2rem; font-weight: bold; }
        .nav-links { display: flex; gap: 15px; }
        .nav-links a {
            color: white;
            text-decoration: none;
            padding: 6px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
        }
        .nav-links a:hover { background: rgba(255, 255, 255, 0.1); }
        .container { max-width: 500px; margin: 0 auto; padding: 20px; }
        .back-btn {
            display: inline-block;
            margin-bottom: 15px;
            color: white;
            text-decoration: none;
            padding: 8px 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            font-size: 0.85rem;
        }
        .back-btn:hover { background: rgba(255, 255, 255, 0.2); }
        
        .pokemon-card {
            background: linear-gradient(135deg, #2d1b4e 0%, #1a1a2e 100%);
            border-radius: 20px;
            padding: 20px;
            text-align: center;
        }
        
        /* Rarity border */
        .pokemon-card.rarity-common { border: 2px solid #a0a0a0; }
        .pokemon-card.rarity-uncommon { border: 2px solid #4cd137; }
        .pokemon-card.rarity-rare { border: 2px solid #00a8ff; }
        .pokemon-card.rarity-epic { border: 2px solid #9c88ff; }
        .pokemon-card.rarity-legendary { 
            border: 2px solid #ffd700;
            animation: legendary-glow 2s ease-in-out infinite;
        }
        
        @keyframes legendary-glow {
            0%, 100% { box-shadow: 0 0 10px #ffd700, 0 0 20px #ffa502; }
            50% { box-shadow: 0 0 15px #ffd700, 0 0 30px #ffa502; }
        }
        
        .pokemon-image { font-size: 5rem; margin-bottom: 10px; }
        .pokemon-name { font-size: 1.8rem; font-weight: bold; margin-bottom: 8px; }
        
        .shiny-badge {
            display: inline-block;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            color: #000;
            padding: 3px 10px;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.7rem;
            margin-left: 8px;
            animation: shiny-glow 1.5s ease-in-out infinite;
        }
        
        @keyframes shiny-glow {
            0%, 100% { box-shadow: 0 0 5px #ffd700; }
            50% { box-shadow: 0 0 10px #ffd700, 0 0 15px #ff8c00; }
        }
        
        .type-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 12px;
            margin: 3px;
            font-size: 0.8rem;
            font-weight: bold;
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
            padding: 4px 12px;
            border-radius: 10px;
            font-size: 0.75rem;
            font-weight: bold;
            margin: 3px;
        }
        .rarity-common-badge { background: #6c757d; }
        .rarity-uncommon-badge { background: #28a745; }
        .rarity-rare-badge { background: #007bff; }
        .rarity-epic-badge { background: #6f42c1; }
        .rarity-legendary-badge { background: linear-gradient(45deg, #ffd700, #ff8c00); color: #000; }
        
        .info-section {
            margin-top: 15px;
            text-align: left;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 15px;
        }
        
        .info-section h3 {
            margin-bottom: 10px;
            font-size: 1rem;
            color: #4ecdc4;
        }
        
        .info-row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.85rem;
        }
        
        .info-label { opacity: 0.7; }
        .info-value { font-weight: bold; }
        
        .description {
            font-style: italic;
            opacity: 0.8;
            line-height: 1.5;
            margin-top: 10px;
            font-size: 0.85rem;
        }
        
        .locked-message {
            background: rgba(255, 0, 0, 0.2);
            border: 2px solid #ff6b6b;
            border-radius: 12px;
            padding: 15px;
            margin-top: 15px;
            text-align: center;
        }
        
        .locked-message h2 { color: #ff6b6b; margin-bottom: 8px; font-size: 1.1rem; }
        
        .unlocked-badge {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
            padding: 6px 15px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: bold;
            display: inline-block;
            margin-top: 12px;
        }
        
        .collection-count {
            margin-top: 12px;
            padding: 10px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">⚔️ Pokemon Trainer</div>
        <div class="nav-links">
            <a href="{% url 'pokemon:dashboard' %}">Dashboard</a>
            <a href="{% url 'pokemon:pokedex' %}">Pokédex</a>
            <a href="{% url 'pokemon:my_team' %}">My Team</a>
            <a href="{% url 'pokemon:profile' %}">Profile</a>
            <a href="{% url 'pokemon:logout' %}">Logout</a>
        </div>
    </nav>
    
    <div class="container">
        <a href="{% url 'pokemon:pokedex' %}" class="back-btn">← Back</a>
        
        <div class="pokemon-card rarity-{{ pokemon.rarity|lower }}">
            <div class="pokemon-image">
                🐾{% if is_shiny %}<span style="font-size: 2rem;">⭐</span>{% endif %}
            </div>
            
            <h1 class="pokemon-name">
                {{ pokemon.name }}
                {% if is_shiny %}
                <span class="shiny-badge">SHINY</span>
                {% endif %}
            </h1>
            
            <div>
                <span class="type-badge type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}-badge">{{ pokemon.rarity }}</span>
            </div>
            
            {% if is_unlocked %}
            <div class="unlocked-badge">✓ Unlocked</div>
            
            <div class="info-section">
                <h3>📊 Details</h3>
                <div class="info-row">
                    <span class="info-label">Name</span>
                    <span class="info-value">{{ pokemon.name }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Type</span>
                    <span class="info-value">{{ pokemon.type }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Rarity</span>
                    <span class="info-value">{{ pokemon.rarity }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Level Req</span>
                    <span class="info-value">Level {{ pokemon.level_requirement }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Shiny</span>
                    <span class="info-value">{% if is_shiny %}⭐ Yes{% else %}No{% endif %}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Obtained</span>
                    <span class="info-value">{{ all_unlocks.count }}x</span>
                </div>
                
                {% if pokemon.description %}
                <h3 style="margin-top: 12px;">📝 Description</h3>
                <p class="description">{{ pokemon.description }}</p>
                {% endif %}
            </div>
            
            {% if all_unlocks.count > 1 %}
            <div class="collection-count">
                <p>📦 {{ all_unlocks.count }} copies ({{ all_unlocks.count|add:-1 }} dupes)</p>
            </div>
            {% endif %}
            
            {% else %}
            <div class="locked-message">
                <h2>🔒 Locked</h2>
                <p>Reach Level {{ pokemon.level_requirement }} to unlock!</p>
            </div>
            
            <div class="info-section">
                <h3>📊 Details</h3>
                <div class="info-row">
                    <span class="info-label">Name</span>
                    <span class="info-value">{{ pokemon.name }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Type</span>
                    <span class="info-value">{{ pokemon.type }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Rarity</span>
                    <span class="info-value">{{ pokemon.rarity }}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Level Req</span>
                    <span class="info-value">Level {{ pokemon.level_requirement }}</span>
                </div>
                
                {% if pokemon.description %}
                <h3 style="margin-top: 12px;">📝 Description</h3>
                <p class="description">{{ pokemon.description }}</p>
                {% endif %}
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

with open('quickserve/pokemon/templates/pokemon/pokemon_detail.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('pokemon_detail.html fixed - smaller now!')
