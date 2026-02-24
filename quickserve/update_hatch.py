# This script updates the hatch_egg function in views.py

old_code = '''    # Check if trainer has eggs
    if trainer.egg_count <= 0:
        messages.error(request, 'You have no eggs to hatch!')
        return redirect('pokemon:dashboard')
    
    # Get ALL Pokemon (not just unlocked) - gacha style
    all_pokemon = Pokemon.objects.all()
    
    if not all_pokemon:
        messages.error(request, 'No Pokemon available!')
        return redirect('pokemon:dashboard')
    
    # Pick a random Pokemon from all Pokemon
    random_pokemon = random.choice(all_pokemon)
    
    # Auto-unlock this Pokemon for the trainer
    PokemonUnlock.objects.get_or_create(trainer=trainer, pokemon=random_pokemon)
    
    # Decrease egg count
    trainer.egg_count -= 1
    trainer.save()
    
    # Add XP for hatching (small bonus)
    trainer.add_xp(10)'''

new_code = '''    # Check if trainer has eggs
    if trainer.egg_count <= 0:
        messages.error(request, 'You have no eggs to hatch!')
        return redirect('pokemon:dashboard')
    
    # Rarity chances: Common 50%, Uncommon 25%, Rare 15%, Epic 8%, Legendary 2%
    rarity_chances = {'Common': 50, 'Uncommon': 25, 'Rare': 15, 'Epic': 8, 'Legendary': 2}
    
    # Get Pokemon by rarity based on chances
    rand = random.randint(1, 100)
    cumulative = 0
    selected_rarity = 'Common'
    for rarity, chance in rarity_chances.items():
        cumulative += chance
        if rand <= cumulative:
            selected_rarity = rarity
            break
    
    # Get Pokemon of the selected rarity
    pokemon_pool = Pokemon.objects.filter(rarity=selected_rarity)
    if not pokemon_pool.exists():
        pokemon_pool = Pokemon.objects.all()
    
    # Pick a random Pokemon from the pool
    random_pokemon = random.choice(pokemon_pool)
    
    # Check if already unlocked
    already_unlocked = trainer.unlocks.filter(pokemon=random_pokemon).exists()
    
    # Auto-unlock this Pokemon for the trainer (even if duplicate)
    PokemonUnlock.objects.get_or_create(trainer=trainer, pokemon=random_pokemon)
    
    # Decrease egg count
    trainer.egg_count -= 1
    trainer.save()
    
    # Add XP for hatching (bonus based on rarity)
    xp_bonus = {'Common': 5, 'Uncommon': 10, 'Rare': 15, 'Epic': 25, 'Legendary': 50}
    trainer.add_xp(xp_bonus.get(selected_rarity, 10))'''

with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(old_code, new_code)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done updating hatch_egg function')
