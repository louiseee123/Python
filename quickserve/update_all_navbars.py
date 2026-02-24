# Script to update all templates with inventory link and logout icon

import os
import re

# CSS to add to all templates
logout_icon_css = '''
        .logout-icon { display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; background: rgba(255,255,255,0.1); transition: all 0.3s; text-decoration: none; }
        .logout-icon:hover { background: rgba(255,100,100,0.3); transform: scale(1.1); }
        .logout-icon svg { width: 20px; height: 20px; fill: white; }'''

# Navbar HTML to replace (simple version without active class)
old_nav_simple = '''            <a href="{% url 'pokemon:logout' %}">Logout</a>'''

new_nav_with_inventory = '''            <a href="{% url 'pokemon:inventory' %}">Inventory</a>
            <a href="{% url 'pokemon:achievements' %}">Achievements</a>
            <a href="{% url 'pokemon:logout' %}" class="logout-icon" title="Logout">
                <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path d="M17 7l-1.41 1.41L18.17 11H8v2h10.17l-2.58 2.58L17 17l5-5zM4 5h8V3H4c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h8v-2H4V5z"/>
                </svg>
            </a>'''

# Templates to update (list of file paths relative to quickserve/)
templates_to_update = [
    'pokemon/templates/pokemon/pokedex.html',
    'pokemon/templates/pokemon/my_team_updated.html',
    'pokemon/templates/pokemon/profile_new.html',
    'pokemon/templates/pokemon/shop.html',
    'pokemon/templates/pokemon/safari_zone.html',
    'pokemon/templates/pokemon/achievements.html',
    'pokemon/templates/pokemon/pokemon_detail.html',
    'pokemon/templates/pokemon/hatch_result.html',
    'pokemon/templates/pokemon/admin_panel.html',
]

def update_template(filepath):
    if not os.path.exists(filepath):
        print(f"  Skipping {filepath} - not found")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Check if already has logout-icon
    if 'logout-icon' in content:
        print(f"  Skipping {filepath} - already has logout-icon")
        return False
    
    # Add logout-icon CSS after .nav-links a.active
    if '.nav-links a.active' in content:
        content = content.replace(
            '.nav-links a.active { background: rgba(78,205,196,0.3); }',
            '.nav-links a.active { background: rgba(78,205,196,0.3); }' + logout_icon_css
        )
    
    # Update navbar - replace Logout with Inventory + Achievements + Logout icon
    if old_nav_simple in content:
        content = content.replace(old_nav_simple, new_nav_with_inventory)
        print(f"  Updated: {filepath}")
        return True
    else:
        print(f"  Could not find logout link in: {filepath}")
        return False

# Update all templates
print("Updating templates with Inventory link and Logout icon...\n")

base_path = 'c:/Users/Windows 10 Pro/Documents/EDP/Python/quickserve/'
success_count = 0

for template_path in templates_to_update:
    full_path = os.path.join(base_path, template_path)
    if update_template(full_path):
        success_count += 1
        # Write back
        with open(full_path, 'w', encoding='utf-8') as f:
            with open(full_path, 'r', encoding='utf-8') as rf:
                f.write(rf.read())

print(f"\nDone! Updated {success_count} templates.")
