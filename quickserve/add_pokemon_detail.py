# Add Pokemon detail view and URL

# First, update urls.py to add the detail route
with open('pokemon/urls.py', 'r', encoding='utf-8') as f:
    urls_content = f.read()

# Add detail URL if not exists
if "path('pokemon/<int:pokemon_id>/', views.pokemon_detail" not in urls_content:
    old_urls = '''    # Egg Gacha
    path('hatch-egg/', views.hatch_egg, name='hatch_egg'),'''
    
    new_urls = '''    # Egg Gacha
    path('hatch-egg/', views.hatch_egg, name='hatch_egg'),
    
    # Pokemon Detail
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),'''
    
    urls_content = urls_content.replace(old_urls, new_urls)
    
    with open('pokemon/urls.py', 'w', encoding='utf-8') as f:
        f.write(urls_content)
    
    print('URL route added')
else:
    print('URL route already exists')

# Now add the view function
with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    views_content = f.read()

# Add pokemon_detail view if not exists
if 'def pokemon_detail' not in views_content:
    # Add import for get_object_or_404 if needed
    views_content = views_content.replace(
        'from django.shortcuts import render, redirect, get_object_or_404',
        'from django.shortcuts import render, redirect, get_object_or_404'
    )
    
    # Add the view function before hatch_egg
    detail_view = '''

@login_required
def pokemon_detail(request, pokemon_id):
    """Show detailed info about a specific Pokemon."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    # Get the Pokemon
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    
    # Check if unlocked
    unlock = trainer.unlocks.filter(pokemon=pokemon).first()
    is_unlocked = unlock is not None
    is_shiny = unlock.shiny if unlock else False
    
    # Get all unlock instances for this trainer (to handle duplicates)
    all_unlocks = trainer.unlocks.filter(pokemon=pokemon)
    
    context = {
        'pokemon': pokemon,
        'is_unlocked': is_unlocked,
        'is_shiny': is_shiny,
        'all_unlocks': all_unlocks,
    }
    
    return render(request, 'pokemon/pokemon_detail.html', context)


'''
    
    # Insert before hatch_egg function
    views_content = views_content.replace(
        'def hatch_egg(request):',
        detail_view + 'def hatch_egg(request):'
    )
    
    with open('pokemon/views.py', 'w', encoding='utf-8') as f:
        f.write(views_content)
    
    print('View function added')
else:
    print('View function already exists')
