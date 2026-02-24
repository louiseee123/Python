# Update hatch_egg view to add shiny chance

with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''    # Check if already unlocked
    already_unlocked = trainer.unlocks.filter(pokemon=random_pokemon).exists()
    
    # Auto-unlock this Pokemon for the trainer (even if duplicate)
    PokemonUnlock.objects.get_or_create(trainer=trainer, pokemon=random_pokemon)'''

new = '''    # Check if already unlocked (for non-shiny)
    already_unlocked = trainer.unlocks.filter(pokemon=random_pokemon, shiny=False).exists()
    
    # Check for shiny (1% chance)
    is_shiny = random.randint(1, 100) == 1
    
    # Auto-unlock this Pokemon for the trainer (even if duplicate)
    unlock, created = PokemonUnlock.objects.get_or_create(
        trainer=trainer, 
        pokemon=random_pokemon,
        defaults={'shiny': is_shiny}
    )
    # If already exists and this one is shiny, update it
    if not created and is_shiny and not unlock.shiny:
        unlock.shiny = True
        unlock.save()'''

content = content.replace(old, new)

# Also update the context to include shiny
old2 = '''    # Render the hatch result page
    context = {
        'pokemon': random_pokemon,
        'added_to_team': added_to_team,
        'rarity': selected_rarity,
        'xp_earned': xp_earned,
        'already_unlocked': already_unlocked,
    }
    return render(request, 'pokemon/hatch_result.html', context)'''

new2 = '''    # Extra XP for shiny Pokemon
    if is_shiny:
        xp_earned *= 2  # Double XP for shiny!
    
    # Render the hatch result page
    context = {
        'pokemon': random_pokemon,
        'added_to_team': added_to_team,
        'rarity': selected_rarity,
        'xp_earned': xp_earned,
        'already_unlocked': already_unlocked,
        'is_shiny': is_shiny,
    }
    return render(request, 'pokemon/hatch_result.html', context)'''

content = content.replace(old2, new2)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Views updated with shiny chance')
