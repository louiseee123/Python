# Update hatch_result.html to use sprite images

hatch_content = '''{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Egg Hatched! - Pokémon Trainer</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container { text-align: center; padding: 30px; }
        h1 {
            font-size: 2.5rem;
            margin-bottom: 25px;
            color: #f1c40f;
            text-shadow: 0 0 20px rgba(241, 196, 15, 0.5);
        }
        .pokemon-card {
            background: linear-gradient(135deg, #2d1b4e 0%, #1a1a2e 100%);
            border: 3px solid #9b59b6;
            border-radius: 25px;
            padding: 30px;
            max-width: 400px;
            margin: 0 auto;
        }
        .pokemon-image {
            width: 180px;
            height: 180px;
            margin: 0 auto 15px;
            object-fit: contain;
            animation: bounce 1s ease infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-15px); }
        }
        .pokemon-name {
            font-size: 2rem;
            font-weight: bold;
            margin-bottom: 8px;
            color: #e74c3c;
        }
        .pokemon-type {
            font-size: 1rem;
            opacity: 0.8;
            margin-bottom: 15px;
        }
        .pokemon-type span {
            background: rgba(255, 255, 255, 0.2);
            padding: 4px 12px;
            border-radius: 15px;
            margin: 0 4px;
        }
        .pokemon-desc {
            font-size: 0.9rem;
            opacity: 0.7;
            margin-bottom: 20px;
            font-style: italic;
        }
        .xp-badge {
            background: linear-gradient(135deg, #f1c40f, #f39c12);
            color: #1a1a2e;
            padding: 8px 16px;
            border-radius: 15px;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 15px;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 20px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: bold;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
            transition: all 0.3s ease;
        }
        .btn-primary { background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; }
        .btn-primary:hover { transform: scale(1.05); }
        .btn-secondary { background: rgba(255, 255, 255, 0.2); color: white; }
        .btn-secondary:hover { background: rgba(255, 255, 255, 0.3); }

        .rarity-badge {
            padding: 6px 12px;
            border-radius: 12px;
            margin-bottom: 12px;
            font-weight: bold;
            display: inline-block;
        }
        .rarity-common { background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; }
        .rarity-uncommon { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .rarity-rare { background: linear-gradient(135deg, #3498db, #2980b9); color: white; }
        .rarity-epic { background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; }
        .rarity-legendary { 
            background: linear-gradient(135deg, #f1c40f, #f39c12); 
            color: #1a1a2e; 
            animation: legendary-glow 2s ease-in-out infinite;
        }

        @keyframes legendary-glow {
            0%, 100% { box-shadow: 0 0 15px #ffd700, 0 0 30px #ffa502; }
            50% { box-shadow: 0 0 25px #ffd700, 0 0 45px #ffa502; }
        }

        .pokemon-card.legendary {
            border-color: #ffd700;
            animation: legendary-glow 2s ease-in-out infinite;
        }

        .added-to-team { color: #2ecc71; font-weight: bold; margin-top: 8px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎉 Egg Hatched! 🎉</h1>
        
        <div class="pokemon-card{% if rarity == 'Legendary' %} legendary{% endif %}">
            <img src="{{ pokemon.sprite_url }}" alt="{{ pokemon.name }}" class="pokemon-image">
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
            
            <p style="margin-top: 12px; font-size: 1rem;">Rarity: <strong>{{ rarity }}</strong></p>
            
            {% if added_to_team %}
            <div class="added-to-team">✓ Added to your team!</div>
            {% elif duplicate_pokemon %}
            <div style="margin-top: 8px; color: #f39c12; font-size: 0.85rem;">
                Already in team - found in Pokédex!
            </div>
            {% else %}
            <div style="margin-top: 8px; opacity: 0.7; font-size: 0.85rem;">
                Team is full - add from Pokédex
            </div>
            {% endif %}
            
            {% if already_unlocked and not added_to_team %}
            <div style="margin-top: 5px; opacity: 0.7; font-size: 0.8rem;">
                (You already had this Pokemon)
            </div>
            {% endif %}
            
            <div style="margin-top: 20px;">
                <a href="{% url 'pokemon:dashboard' %}" class="btn btn-primary">Back to Dashboard</a>
                <a href="{% url 'pokemon:pokedex' %}" class="btn btn-secondary">View Pokédex</a>
            </div>
        </div>
    </div>
</body>
</html>
'''

with open('quickserve/pokemon/templates/pokemon/hatch_result.html', 'w', encoding='utf-8') as f:
    f.write(hatch_content)

print('Updated hatch_result.html with sprite images!')
