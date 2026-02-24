# Update hatch_egg to pass xp_earned and already_unlocked

with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    # Render the hatch result page
    context = {
        'pokemon': random_pokemon,
        'added_to_team': added_to_team,
        'rarity': selected_rarity,
    }
    return render(request, 'pokemon/hatch_result.html', context)'''

new = '''    # Get XP earned
    xp_earned = xp_bonus.get(selected_rarity, 10)
    
    # Render the hatch result page
    context = {
        'pokemon': random_pokemon,
        'added_to_team': added_to_team,
        'rarity': selected_rarity,
        'xp_earned': xp_earned,
        'already_unlocked': already_unlocked,
    }
    return render(request, 'pokemon/hatch_result.html', context)'''

content = content.replace(old, new)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
