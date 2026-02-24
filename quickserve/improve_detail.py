# Improve pokemon_detail.html with real Pokedex layout and jumping animation

detail_content = '''{% load static %}
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
        
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
        }
        
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
        
        /* Pokedex-style card with split layout */
        .pokedex-card {
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 50%, #dc2626 100%);
            border-radius: 20px;
            padding: 0;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
            min-height: 400px;
        }
        
        /* Left side - Image */
        .pokedex-left {
            background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
            padding: 30px;
            text-align: center;
            position: relative;
        }
        
        .pokedex-screen {
            background: #1a1a1a;
            border-radius: 15px;
            padding: 20px;
            box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
            border: 4px solid #333;
        }
        
        .pokedex-screen-inner {
            background: linear-gradient(180deg, #2d3748 0%, #1a202c 100%);
            border-radius: 10px;
            padding: 15px;
            min-height: 200px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .pokemon-image { 
            width: 180px; 
            height: 180px;
            object-fit: contain;
            animation: pokemon-bounce 2s ease-in-out infinite;
        }
        
        @keyframes pokemon-bounce {
            0%, 100% { transform: translateY(0) scale(1); }
            25% { transform: translateY(-15px) scale(1.05); }
            50% { transform: translateY(0) scale(1); }
            75% { transform: translateY(-8px) scale(1.02); }
        }
        
        .pokemon-number {
            position: absolute;
            top: 15px;
            left: 15px;
            background: #000;
            color: #fff;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9rem;
        }
        
        .shiny-indicator {
            position: absolute;
            top: 15px;
            right: 15px;
            background: linear-gradient(45deg, #ffd700, #ff8c00);
            color: #000;
            padding: 5px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.8rem;
            animation: shiny-glow 1.5s ease-in-out infinite;
        }
        
        @keyframes shiny-glow {
            0%, 100% { box-shadow: 0 0 5px #ffd700; }
            50% { box-shadow: 0 0 15px #ffd700, 0 0 25px #ff8c00; }
        }
        
        /* Rarity glow */
        .pokedex-screen.rarity-legendary { 
            border-color: #ffd700;
            box-shadow: inset 0 0 30px rgba(255, 215, 0, 0.3), 0 0 20px rgba(255, 215, 0, 0.3);
        }
        
        /* Right side - Details */
        .pokedex-right {
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
            padding: 30px;
        }
        
        .pokemon-name { 
            font-size: 2.5rem; 
            font-weight: bold; 
            margin-bottom: 5px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .pokemon-name-ja {
            font-size: 1rem;
            opacity: 0.7;
            margin-bottom: 15px;
        }
        
        .type-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .type-badge {
            display: inline-block;
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
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
            padding: 6px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .rarity-common { background: #6c757d; }
        .rarity-uncommon { background: #28a745; }
        .rarity-rare { background: #007bff; }
        .rarity-epic { background: #6f42c1; }
        .rarity-legendary { 
            background: linear-gradient(45deg, #ffd700, #ff8c00); 
            color: #000;
            animation: legendary-pulse 2s ease-in-out infinite;
        }
        
        @keyframes legendary-pulse {
            0%, 100% { box-shadow: 0 0 5px #ffd700; }
            50% { box-shadow: 0 0 20px #ffd700, 0 0 30px #ff8c00; }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }
        
        .stat-box {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 12px;
        }
        
        .stat-label {
            font-size: 0.75rem;
            opacity: 0.7;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-value {
            font-size: 1.3rem;
            font-weight: bold;
        }
        
        .description-box {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 15px;
            margin-top: 15px;
        }
        
        .description-text {
            font-style: italic;
            line-height: 1.6;
            opacity: 0.9;
        }
        
        .unlocked-badge {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: bold;
            display: inline-block;
            margin-top: 15px;
        }
        
        .locked-badge {
            background: linear-gradient(135deg, #6c757d, #495057);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: bold;
            display: inline-block;
            margin-top: 15px;
        }
        
        .collection-info {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 12px;
            margin-top: 15px;
            font-size: 0.9rem;
        }
        
        /* Responsive */
        @media (max-width: 600px) {
            .pokedex-card {
                flex-direction: column;
            }
            .pokedex-left, .pokedex-right {
                width: 100%;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
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
        <a href="{% url 'pokemon:pokedex' %}" class="back-btn">← Back to Pokédex</a>
        
        <div class="pokedex-card" style="display: flex;">
            <!-- Left Side - Image -->
            <div class="pokedex-left">
                <span class="pokemon-number">#{{ pokemon.pokeapi_id }}</span>
                {% if is_shiny %}
                <span class="shiny-indicator">⭐ SHINY</span>
                {% endif %}
                
                <div class="pokedex-screen rarity-{{ pokemon.rarity|lower }}">
                    <div class="pokedex-screen-inner">
                        {% if is_unlocked %}
                        <img src="{{ pokemon.sprite_url }}" alt="{{ pokemon.name }}" class="pokemon-image">
                        {% else %}
                        <div class="pokemon-image" style="font-size: 5rem;">🐾</div>
                        {% endif %}
                    </div>
                </div>
            </div>
            
            <!-- Right Side - Details -->
            <div class="pokedex-right">
                <h1 class="pokemon-name">{{ pokemon.name }}</h1>
                
                <div class="type-container">
                    <span class="type-badge type-{{ pokemon.type|lower }}">{{ pokemon.type }}</span>
                    <span class="rarity-badge rarity-{{ pokemon.rarity|lower }}">{{ pokemon.rarity }}</span>
                </div>
                
                {% if is_unlocked %}
                <div class="unlocked-badge">✓ Unlocked</div>
                {% else %}
                <div class="locked-badge">🔒 Locked</div>
                {% endif %}
                
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Level Required</div>
                        <div class="stat-value">Lv. {{ pokemon.level_requirement }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Shiny</div>
                        <div class="stat-value">{% if is_shiny %}⭐ Yes{% else %}No{% endif %}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Owned</div>
                        <div class="stat-value">{{ all_unlocks.count }}x</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">In Team</div>
                        <div class="stat-value">{% if in_team %}✓ Yes{% else %}—{% endif %}</div>
                    </div>
                </div>
                
                <div class="description-box">
                    <div class="description-text">
                        {% if is_unlocked and pokemon.description %}
                        {{ pokemon.description }}
                        {% else %}
                        This Pokemon is hidden until you reach level {{ pokemon.level_requirement }}.
                        {% endif %}
                    </div>
                </div>
                
                {% if all_unlocks.count > 1 %}
                <div class="collection-info">
                    📦 You have {{ all_unlocks.count }} copies ({{ all_unlocks.count|add:"-1" }} duplicates)
                </div>
                {% endif %}
            </div>
        </div>
    </div>
</body>
</html>
'''

with open('quickserve/pokemon/templates/pokemon/pokemon_detail.html', 'w', encoding='utf-8') as f:
    f.write(detail_content)

print('Improved pokemon_detail.html with Pokedex layout and animation!')
