# Script to fix the create_trainer function in views.py

# Read the file
with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the create_trainer function's POST handling
old_code = '''    if request.method == 'POST':
        trainer = Trainer.objects.create(
            user=request.user,
            level=1,
            experience=0,
            max_team_size=6,
            pokeball_count=10
        )
        # Note: Starter Pokemon will be unlocked when the user chooses one in starter_selection
        # This makes the starter selection meaningful - new trainers start with no Pokemon
        
        messages.success(request, 'Trainer profile created!')
        return redirect('pokemon:starter_selection')
    
    return render(request, 'pokemon/create_trainer.html')'''

new_code = '''    if request.method == 'POST':
        trainer = Trainer.objects.create(
            user=request.user,
            level=1,
            experience=0,
            max_team_size=6,
            pokeball_count=10
        )
        Team.objects.create(trainer=trainer)
        
        # Note: Starter Pokemon will be unlocked when the user chooses one in starter_selection
        # This makes the starter selection meaningful - new trainers start with no Pokemon
        
        messages.success(request, 'Trainer profile created!')
        return redirect('pokemon:starter_selection')
    
    return render(request, 'pokemon/create_trainer.html')'''

content = content.replace(old_code, new_code)

# Write back
with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('File updated successfully!')
