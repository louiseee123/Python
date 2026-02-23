from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import date
import random
from .models import Trainer, Pokemon, Team, TeamMember, PokemonUnlock, DailyTask, TrainerTaskCompletion


def home(request):
    """Landing page - redirects to appropriate page based on auth status."""
    if request.user.is_authenticated:
        try:
            trainer = request.user.trainer
            if not hasattr(trainer, 'team') or trainer.team.members.count() == 0:
                return redirect('pokemon:starter_selection')
            return redirect('pokemon:dashboard')
        except Trainer.DoesNotExist:
            return redirect('pokemon:create_trainer')
    return render(request, 'pokemon/home.html')


def create_trainer(request):
    """Create trainer profile for new users."""
    if request.user.is_authenticated:
        try:
            trainer = request.user.trainer
            return redirect('pokemon:dashboard')
        except Trainer.DoesNotExist:
            pass
    
    if request.method == 'POST':
        trainer = Trainer.objects.create(
            user=request.user,
            level=1,
            experience=0,
            max_team_size=6,
            pokeball_count=10
        )
        Team.objects.create(trainer=trainer)
        
        starter_pokemon = Pokemon.objects.filter(is_starter=True)
        for pokemon in starter_pokemon:
            PokemonUnlock.objects.create(trainer=trainer, pokemon=pokemon)
        
        messages.success(request, 'Trainer profile created!')
        return redirect('pokemon:starter_selection')
    
    return render(request, 'pokemon/create_trainer.html')


@login_required
def starter_selection(request):
    """Select starter Pokemon."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    team = trainer.team
    if team.members.count() > 0:
        return redirect('pokemon:dashboard')
    
    starters = Pokemon.objects.filter(is_starter=True)
    
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        pokemon = get_object_or_404(Pokemon, id=pokemon_id, is_starter=True)
        
        unlock, created = PokemonUnlock.objects.get_or_create(
            trainer=trainer,
            pokemon=pokemon
        )
        
        TeamMember.objects.create(
            team=team,
            pokemon=pokemon,
            nickname=pokemon.name
        )
        
        trainer.add_xp(50)
        
        messages.success(request, f'You chose {pokemon.name}!')
        return redirect('pokemon:dashboard')
    
    context = {
        'starters': starters,
    }
    return render(request, 'pokemon/starter_selection.html', context)


@login_required
def dashboard(request):
    """Trainer dashboard/homepage."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    team = trainer.team
    team_members = team.members.all()[:3]
    
    unlocked_count = trainer.unlocks.count()
    total_pokemon = Pokemon.objects.count()
    
    today = date.today()
    daily_tasks = DailyTask.objects.filter(is_active=True)
    
    completed_tasks = TrainerTaskCompletion.objects.filter(
        trainer=trainer,
        date=today
    ).values_list('task_id', flat=True)
    
    login_task = DailyTask.objects.filter(task_type='login').first()
    if login_task and login_task.id not in completed_tasks:
        TrainerTaskCompletion.objects.get_or_create(
            trainer=trainer,
            task=login_task,
            date=today
        )
        trainer.add_xp(login_task.xp_reward)
        if login_task.egg_reward > 0:
            trainer.egg_count += login_task.egg_reward
            trainer.save()
        completed_tasks = list(completed_tasks) + [login_task.id]
    
    legendaries = list(Pokemon.objects.filter(rarity='Legendary'))
    if len(legendaries) >= 8:
        gacha_legendaries = random.sample(legendaries, 8)
    else:
        gacha_legendaries = legendaries
    
    context = {
        'trainer': trainer, 'team_size': team.members.count(), 'max_team_size': trainer.max_team_size,
        'team_members': team_members,
        'unlocked_count': unlocked_count,
        'total_pokemon': total_pokemon,
        'daily_tasks': daily_tasks,
        'completed_tasks': completed_tasks,
        'gacha_legendaries': gacha_legendaries,
    }
    return render(request, 'pokemon/dashboard.html', context)


@login_required
def pokedex(request):
    """Pokédex view showing all Pokemon with lock/unlock status."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    pokemon_type = request.GET.get('type')
    search_query = request.GET.get('search')
    
    unlocked_data = {}
    for unlock in trainer.unlocks.all():
        unlocked_data[unlock.pokemon_id] = unlock.shiny
    
    pokemon_list = Pokemon.objects.all()
    
    if pokemon_type:
        pokemon_list = pokemon_list.filter(type=pokemon_type)
    if search_query:
        pokemon_list = pokemon_list.filter(name__icontains=search_query)
    
    types = Pokemon.TYPES
    team_pokemon_ids = set(trainer.team.members.values_list('pokemon_id', flat=True))
    
    context = {
        'pokemon_list': pokemon_list,
        'unlocked_ids': set(unlocked_data.keys()),
        'unlocked_data': unlocked_data,
        'types': types,
        'selected_type': pokemon_type,
        'search_query': search_query,
        'trainer': trainer, 'team_size': team.members.count(), 'max_team_size': trainer.max_team_size,
        'team_pokemon_ids': team_pokemon_ids,
    }
    return render(request, 'pokemon/pokedex.html', context)


@login_required
def my_team(request):
    """My Team view for managing team members."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    team = trainer.team
    members = team.members.all()
    
    unlocked_pokemon = trainer.unlocks.select_related('pokemon')
    team_pokemon_ids = team.members.values_list('pokemon_id', flat=True)
    available_pokemon = []
    for u in unlocked_pokemon:
        if u.pokemon.id not in team_pokemon_ids:
            available_pokemon.append((u.pokemon, u.shiny, u.unlocked_at))
    
    team_shiny = {}
    for member in members:
        unlock = trainer.unlocks.filter(pokemon=member.pokemon).first()
        team_shiny[member.id] = unlock.shiny if unlock else False
    
    context = {
        'trainer': trainer, 'team_size': team.members.count(), 'max_team_size': trainer.max_team_size,
        'team': team,
        'members': members,
        'team_shiny': team_shiny,
        'available_pokemon': available_pokemon,
    }
    return render(request, 'pokemon/my_team.html', context)


@login_required
def add_to_team(request, pokemon_id):
    """Add Pokemon to team."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    team = trainer.team
    
    if team.is_full:
        messages.error(request, f'Your team is full! Max size: {trainer.max_team_size}')
        return redirect('pokemon:pokedex')
    
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    
    if not trainer.unlocks.filter(pokemon=pokemon).exists():
        PokemonUnlock.objects.get_or_create(trainer=trainer, pokemon=pokemon)
    
    if team.members.filter(pokemon=pokemon).exists():
        messages.error(request, 'This Pokemon is already in your team!')
        return redirect('pokemon:my_team')
    
    TeamMember.objects.create(
        team=team,
        pokemon=pokemon,
        nickname=pokemon.name
    )
    
    add_team_task = DailyTask.objects.filter(task_type='add_team').first()
    if add_team_task:
        today = date.today()
        if not TrainerTaskCompletion.objects.filter(trainer=trainer, task=add_team_task, date=today).exists():
            TrainerTaskCompletion.objects.create(trainer=trainer, task=add_team_task, date=today)
            trainer.add_xp(add_team_task.xp_reward)
            if add_team_task.egg_reward > 0:
                trainer.egg_count += add_team_task.egg_reward
                trainer.save()
            messages.success(request, f'Added {pokemon.name} to team! +{add_team_task.xp_reward} XP, +{add_team_task.egg_reward} Egg(s)')
        else:
            messages.success(request, f'Added {pokemon.name} to team!')
    else:
        messages.success(request, f'Added {pokemon.name} to team!')
    
    return redirect('pokemon:my_team')


@login_required
def remove_from_team(request, member_id):
    """Remove Pokemon from team."""
    member = get_object_or_404(TeamMember, id=member_id, team__trainer=request.user.trainer)
    pokemon_name = member.pokemon.name
    member.delete()
    messages.success(request, f'{pokemon_name} removed from team!')
    return redirect('pokemon:my_team')


@login_required
def rename_member(request, member_id):
    """Rename a team member."""
    member = get_object_or_404(TeamMember, id=member_id, team__trainer=request.user.trainer)
    
    if request.method == 'POST':
        new_nickname = request.POST.get('nickname', '').strip()
        member.nickname = new_nickname if new_nickname else None
        member.save()
        messages.success(request, 'Nickname updated!')
        return redirect('pokemon:my_team')
    
    context = {
        'member': member,
    }
    return render(request, 'pokemon/rename_member.html', context)


@login_required
def claim_task_xp(request, task_id):
    """Claim XP and eggs for completing a task."""
    task = get_object_or_404(DailyTask, id=task_id)
    trainer = request.user.trainer
    today = date.today()
    
    if TrainerTaskCompletion.objects.filter(trainer=trainer, task=task, date=today).exists():
        messages.error(request, 'Task already completed!')
        return redirect('pokemon:dashboard')
    
    TrainerTaskCompletion.objects.create(trainer=trainer, task=task, date=today)
    trainer.add_xp(task.xp_reward)
    
    if task.egg_reward > 0:
        trainer.egg_count += task.egg_reward
        trainer.save()
        messages.success(request, f'Task completed! +{task.xp_reward} XP, +{task.egg_reward} Egg(s)')
    else:
        messages.success(request, f'Task completed! +{task.xp_reward} XP')
    
    return redirect('pokemon:dashboard')


@login_required
def pokemon_detail(request, pokemon_id):
    """Show detailed info about a specific Pokemon."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    team = trainer.team
    
    unlock = trainer.unlocks.filter(pokemon=pokemon).first()
    is_unlocked = unlock is not None
    is_shiny = unlock.shiny if unlock else False
    all_unlocks = trainer.unlocks.filter(pokemon=pokemon)
    in_team = team.members.filter(pokemon=pokemon).exists()
    
    context = {
        'pokemon': pokemon,
        'is_unlocked': is_unlocked,
        'is_shiny': is_shiny,
        'all_unlocks': all_unlocks,
        'in_team': in_team,
    }
    
    return render(request, 'pokemon/pokemon_detail.html', context)


def hatch_egg(request):
    """Hatch an egg to get a random Pokemon."""
    trainer = request.user.trainer
    
    if trainer.egg_count <= 0:
        messages.error(request, 'You have no eggs to hatch!')
        return redirect('pokemon:dashboard')
    
    rarity_chances = {'Common': 50, 'Uncommon': 25, 'Rare': 15, 'Epic': 8, 'Legendary': 2}
    
    rand = random.randint(1, 100)
    cumulative = 0
    selected_rarity = 'Common'
    for rarity, chance in rarity_chances.items():
        cumulative += chance
        if rand <= cumulative:
            selected_rarity = rarity
            break
    
    pokemon_pool = Pokemon.objects.filter(rarity=selected_rarity)
    if not pokemon_pool.exists():
        pokemon_pool = Pokemon.objects.all()
    
    random_pokemon = random.choice(pokemon_pool)
    already_unlocked = trainer.unlocks.filter(pokemon=random_pokemon, shiny=False).exists()
    shiny_chance = getattr(trainer, 'shiny_luck', 1)
    is_shiny = random.randint(1, 100) <= shiny_chance
    
    unlock, created = PokemonUnlock.objects.get_or_create(
        trainer=trainer, 
        pokemon=random_pokemon,
        defaults={'shiny': is_shiny}
    )
    if not created and is_shiny and not unlock.shiny:
        unlock.shiny = True
        unlock.save()
    
    trainer.egg_count -= 1
    trainer.save()
    
    xp_bonus = {'Common': 5, 'Uncommon': 10, 'Rare': 15, 'Epic': 25, 'Legendary': 50}
    trainer.add_xp(xp_bonus.get(selected_rarity, 10))
    
    team = trainer.team
    added_to_team = False
    if not team.is_full:
        if not team.members.filter(pokemon=random_pokemon).exists():
            TeamMember.objects.create(
                team=team,
                pokemon=random_pokemon,
                nickname=random_pokemon.name
            )
            added_to_team = True
    
    xp_earned = xp_bonus.get(selected_rarity, 10)
    if is_shiny:
        xp_earned *= 2
    
    context = {
        'pokemon': random_pokemon,
        'added_to_team': added_to_team,
        'rarity': selected_rarity,
        'xp_earned': xp_earned,
        'already_unlocked': already_unlocked,
        'is_shiny': is_shiny,
    }
    return render(request, 'pokemon/hatch_result.html', context)


@login_required
def profile(request):
    """Trainer profile view."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    team = trainer.team
    members = team.members.all()
    recent_unlocks = trainer.unlocks.select_related('pokemon').order_by('-unlocked_at')[:5]
    
    context = {
        'trainer': trainer, 'team_size': team.members.count(), 'max_team_size': trainer.max_team_size,
        'members': members,
        'recent_unlocks': recent_unlocks,
    }
    return render(request, 'pokemon/profile.html', context)


def signup(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('pokemon:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'pokemon/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'pokemon/signup.html')
        
        user = User.objects.create_user(username=username, password=password)
        
        trainer = Trainer.objects.create(
            user=user,
            level=1,
            experience=0,
            max_team_size=6,
            pokeball_count=10
        )
        Team.objects.create(trainer=trainer)
        
        starter_pokemon = Pokemon.objects.filter(is_starter=True)
        for pokemon in starter_pokemon:
            PokemonUnlock.objects.create(trainer=trainer, pokemon=pokemon)
        
        messages.success(request, 'Account created! Please log in.')
        return redirect('pokemon:login')
    
    return render(request, 'pokemon/signup.html')


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('pokemon:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            from django.contrib.auth import login
            login(request, user)
            return redirect('pokemon:home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'pokemon/login.html')


@login_required
def logout_view(request):
    """User logout."""
    from django.contrib.auth import logout
    logout(request)
    return redirect('pokemon:home')


@login_required
def safari_zone(request):
    """Safari Zone - catch wild Pokemon in the field."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    # Check if we need to generate new weather (every 5 minutes)
    # Store weather in session with timestamp
    session = request.session
    weather_timestamp = session.get('safari_weather_timestamp', 0)
    import time
    current_time = int(time.time())
    
    # 5 minutes = 300 seconds
    if current_time - weather_timestamp > 300:
        # Generate new weather
        weather_options = ['Sunny', 'Cloudy', 'Rainy', 'Foggy']
        weather = random.choice(weather_options)
        session['safari_weather'] = weather
        session['safari_weather_timestamp'] = current_time
    else:
        weather = session.get('safari_weather', 'Sunny')
    
    # Check if we need to refresh Pokemon (but keep weather)
    pokemon_refresh = request.GET.get('refresh', 'false') == 'true'
    
    # Get caught and escaped pokemon from session
    caught_pokemon_ids = session.get('safari_caught_pokemon', [])
    escaped_pokemon_ids = session.get('safari_escaped_pokemon', [])
    
    if pokemon_refresh or 'safari_pokemon' not in session:
        # Generate new wild Pokemon (fresh safari run)
        session['safari_caught_pokemon'] = []
        session['safari_escaped_pokemon'] = []
        
        all_pokemon = list(Pokemon.objects.all())
        if len(all_pokemon) >= 5:
            wild_pokemon = random.sample(all_pokemon, 5)
        else:
            wild_pokemon = all_pokemon
        
        safari_pokemon = []
        for i, pokemon in enumerate(wild_pokemon):
            safari_pokemon.append({
                'pokemon_id': pokemon.id,
                'pokemon_name': pokemon.name,
                'pokemon_sprite': pokemon.sprite_url,
                'pokemon_rarity': pokemon.rarity,
                'duration': random.randint(10, 30),
                'left': random.randint(10, 80),
                'top': random.randint(10, 80),
                'id': i,
            })
        session['safari_pokemon'] = safari_pokemon
    else:
        safari_pokemon = session.get('safari_pokemon', [])
    
    # Filter out caught and escaped pokemon from the list
    excluded_ids = set(caught_pokemon_ids + escaped_pokemon_ids)
    safari_pokemon = [p for p in safari_pokemon if p['pokemon_id'] not in excluded_ids]
    
    # Weather effects on catch rates
    weather_bonus = {
        'Sunny': 5,      # +5% catch rate - Pokemon are happier
        'Cloudy': 0,     # Normal
        'Rainy': 10,     # +10% catch rate - Pokemon seek shelter, easier to catch
        'Foggy': -5,     # -5% catch rate - Harder to find/catch
    }
    
    weather_effect = weather_bonus.get(weather, 0)
    
    # Weather visual effects for the field
    weather_info = {
        'Sunny': {
            'icon': '☀️',
            'effect': '+5% Catch Rate',
            'description': 'Pokemon are willing to bond with trainers in sunny weather!'
        },
        'Cloudy': {
            'icon': '☁️',
            'effect': 'Normal',
            'description': 'Perfect weather for a safari adventure!'
        },
        'Rainy': {
            'icon': '🌧️',
            'effect': '+10% Catch Rate',
            'description': 'Pokemon are seeking shelter - easier to catch!'
        },
        'Foggy': {
            'icon': '🌫️',
            'effect': '-5% Catch Rate',
            'description': 'Pokemon are harder to spot in the fog...'
        },
    }
    
    context = {
        'trainer': trainer, 'team_size': team.members.count(), 'max_team_size': trainer.max_team_size,
        'safari_pokemon': safari_pokemon,
        'weather': weather,
        'weather_effect': weather_effect,
        'weather_info': weather_info.get(weather, weather_info['Sunny']),
    }
    return render(request, 'pokemon/safari_zone.html', context)


@login_required
def catch_pokemon(request, pokemon_id):
    """Attempt to catch a Pokemon in the Safari Zone - returns JSON for AJAX."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No trainer found'})
    
    if trainer.pokeball_count <= 0:
        return JsonResponse({'success': False, 'error': 'No pokeballs left', 'pokeballs': 0})
    
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    
    trainer.pokeball_count -= 1
    
    # Base catch rates by rarity
    catch_rates = {
        'Common': 70,
        'Uncommon': 50,
        'Rare': 35,
        'Epic': 20,
        'Legendary': 10,
    }
    catch_rate = catch_rates.get(pokemon.rarity, 50)
    
    # Get weather bonus from session
    session = request.session
    weather = session.get('safari_weather', 'Sunny')
    weather_bonus = {
        'Sunny': 5,      # +5% catch rate
        'Cloudy': 0,     # Normal
        'Rainy': 10,     # +10% catch rate
        'Foggy': -5,     # -5% catch rate
    }
    weather_effect = weather_bonus.get(weather, 0)
    catch_rate += weather_effect
    
    # Ensure catch rate is within bounds
    catch_rate = max(5, min(95, catch_rate))
    
    catch_roll = random.randint(1, 100)
    
    if catch_roll <= catch_rate:
        # Mark pokemon as caught in session so it doesn't reappear
        caught_pokemon = session.get('safari_caught_pokemon', [])
        if pokemon.id not in caught_pokemon:
            caught_pokemon.append(pokemon.id)
            session['safari_caught_pokemon'] = caught_pokemon
        
        unlock, created = PokemonUnlock.objects.get_or_create(
            trainer=trainer,
            pokemon=pokemon,
            defaults={'shiny': False}
        )
        
        shiny_chance = getattr(trainer, 'shiny_luck', 1)
        is_shiny = random.randint(1, 100) <= shiny_chance
        
        already_unlocked = not created and not unlock.shiny
        
        if is_shiny and not unlock.shiny:
            unlock.shiny = True
            unlock.save()
        
        trainer.save()
        
        xp_bonus = {'Common': 5, 'Uncommon': 10, 'Rare': 15, 'Epic': 25, 'Legendary': 50}
        xp_earned = xp_bonus.get(pokemon.rarity, 10)
        trainer.add_xp(xp_earned)
        
        team = trainer.team
        added_to_team = False
        if not team.is_full:
            if not team.members.filter(pokemon=pokemon).exists():
                TeamMember.objects.create(
                    team=team,
                    pokemon=pokemon,
                    nickname=pokemon.name
                )
                added_to_team = True
        
        return JsonResponse({
            'success': True,
            'caught': True,
            'pokemon_name': pokemon.name,
            'pokemon_sprite': pokemon.sprite_url,
            'rarity': pokemon.rarity,
            'is_shiny': is_shiny,
            'added_to_team': added_to_team,
            'xp_earned': xp_earned,
            'pokeballs': trainer.pokeball_count,
        })
    else:
        # Mark pokemon as escaped in session so it doesn't reappear
        escaped_pokemon = session.get('safari_escaped_pokemon', [])
        if pokemon.id not in escaped_pokemon:
            escaped_pokemon.append(pokemon.id)
            session['safari_escaped_pokemon'] = escaped_pokemon
        
        trainer.save()
        return JsonResponse({
            'success': True,
            'caught': False,
            'pokemon_name': pokemon.name,
            'pokemon_sprite': pokemon.sprite_url,
            'message': f'{pokemon.name} doesn\'t want to get caught and ran away!',
            'pokeballs': trainer.pokeball_count,
        })
