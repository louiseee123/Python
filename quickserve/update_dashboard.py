# Script to update dashboard.html with inventory link and logout icon
import re

# Read the file
with open('pokemon/templates/pokemon/dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add logout-icon CSS
old_css = '''        .nav-links { display: flex; gap: 20px; }
        .nav-links a { color: white; text-decoration: none; padding: 8px 15px; border-radius: 20px; transition: all 0.3s; }
        .nav-links a:hover { background: rgba(255,255,255,0.1); }
        .nav-links a.active { background: rgba(78,205,196,0.3); }'''

new_css = '''        .nav-links { display: flex; gap: 20px; align-items: center; }
        .nav-links a { color: white; text-decoration: none; padding: 8px 15px; border-radius: 20px; transition: all 0.3s; }
        .nav-links a:hover { background: rgba(255,255,255,0.1); }
        .nav-links a.active { background: rgba(78,205,196,0.3); }
        .logout-icon { display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.1); transition: all 0.3s; text-decoration: none; }
        .logout-icon:hover { background: rgba(255,100,100,0.3); transform: scale(1.1); }
        .logout-icon svg { width: 20px; height: 20px; fill: white; }'''

content = content.replace(old_css, new_css)

# Update navbar links
old_nav = '''            <a href="{% url 'pokemon:dashboard' %}" class="active">Dashboard</a>
            <a href="{% url 'pokemon:pokedex' %}">Pokédex</a>
            <a href="{% url 'pokemon:my_team' %}">My Team</a>
            <a href="{% url 'pokemon:profile' %}">Profile</a>
            <a href="{% url 'pokemon:shop' %}">Shop</a>
            <a href="{% url 'pokemon:safari_zone' %}">Safari Zone</a>
            <a href="{% url 'pokemon:logout' %}">Logout</a>'''

new_nav = '''            <a href="{% url 'pokemon:dashboard' %}" class="active">Dashboard</a>
            <a href="{% url 'pokemon:pokedex' %}">Pokédex</a>
            <a href="{% url 'pokemon:my_team' %}">My Team</a>
            <a href="{% url 'pokemon:profile' %}">Profile</a>
            <a href="{% url 'pokemon:shop' %}">Shop</a>
            <a href="{% url 'pokemon:safari_zone' %}">Safari Zone</a>
            <a href="{% url 'pokemon:inventory' %}">Inventory</a>
            <a href="{% url 'pokemon:achievements' %}">Achievements</a>
            <a href="{% url 'pokemon:logout' %}" class="logout-icon" title="Logout">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                </svg>
            </a>'''

content = content.replace(old_nav, new_nav)

# Write back
with open('pokemon/templates/pokemon/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Dashboard updated successfully')
