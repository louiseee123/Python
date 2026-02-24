from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from datetime import date
import random
from .models import Trainer, Pokemon, Team, TeamMember, PokemonUnlock, DailyTask, TrainerTaskCompletion, ShopItem, InventoryItem


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
    
    # Pre-compute pokemon data with unlock status
    unlocked_data = {}
    for unlock in trainer.unlocks.all():
        unlocked_data[unlock.pokemon_id] = {'shiny': unlock.shiny}
    
    pokemon_list = Pokemon.objects.all()
    
    if pokemon_type:
        pokemon_list = pokemon_list.filter(type=pokemon_type)
    if search_query:
        pokemon_list = pokemon_list.filter(name__icontains=search_query)
    
    types = Pokemon.TYPES
    team = trainer.team
    team_pokemon_ids = set(team.members.values_list('pokemon_id', flat=True))
    
    # Pre-compute list of pokemon with status
    pokemon_data = []
    for pokemon in pokemon_list:
        pokemon_data.append({
            'pokemon': pokemon,
            'is_unlocked': pokemon.id in unlocked_data,
            'is_shiny': unlocked_data.get(pokemon.id, {}).get('shiny', False),
            'in_team': pokemon.id in team_pokemon_ids,
        })
    
    context = {
        'pokemon_data': pokemon_data,
        'types': types,
        'selected_type': pokemon_type,
        'search_query': search_query,
        'trainer': trainer, 
        'team_size': team.members.count(), 
        'max_team_size': trainer.max_team_size,
        'total_pokemon': Pokemon.objects.count(),
        'unlocked_count': len(unlocked_data),
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
    return render(request, 'pokemon/my_team_updated.html', context)


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
    
    # Coin values for duplicate Pokemon (only for non-shiny duplicates)
    coin_values = {
        'Common': 100,
        'Uncommon': 250,
        'Rare': 500,
        'Epic': 750,
        'Legendary': 1000,
    }
    
    # Check if this is a duplicate (already unlocked non-shiny)
    is_duplicate = already_unlocked and not is_shiny
    coins_earned = 0
    
    if is_duplicate:
        # Convert duplicate to PokeHunt Coins
        coins_earned = coin_values.get(selected_rarity, 100)
        trainer.hunt_coins += coins_earned
        trainer.save()
    
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
        'duplicate_pokemon': team.members.filter(pokemon=random_pokemon).exists() if not added_to_team else False,
        'is_duplicate': is_duplicate,
        'coins_earned': coins_earned,
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
    
    # Get Pokemon statistics
    all_unlocks = trainer.unlocks.all()
    total_unlocked = all_unlocks.count()
    legendary_unlocked = all_unlocks.filter(pokemon__rarity='Legendary').count()
    epic_unlocked = all_unlocks.filter(pokemon__rarity='Epic').count()
    rare_unlocked = all_unlocks.filter(pokemon__rarity='Rare').count()
    shiny_unlocked = all_unlocks.filter(shiny=True).count()
    
    # Get total Pokemon count
    total_pokemon = Pokemon.objects.count()
    
    # Get team members with their shiny status
    team_members = []
    for member in members:
        unlock = trainer.unlocks.filter(pokemon=member.pokemon).first()
        is_shiny = unlock.shiny if unlock else False
        team_members.append({
            'member': member,
            'is_shiny': is_shiny,
            'pokemon': member.pokemon
        })
    
    context = {
        'trainer': trainer, 'team_size': team.members.count(), 'max_team_size': trainer.max_team_size,
        'members': members,
        'recent_unlocks': recent_unlocks,
        'total_unlocked': total_unlocked,
        'total_pokemon': total_pokemon,
        'legendary_unlocked': legendary_unlocked,
        'epic_unlocked': epic_unlocked,
        'rare_unlocked': rare_unlocked,
        'shiny_unlocked': shiny_unlocked,
        'team_members': team_members,
    }
    return render(request, 'pokemon/profile.html', context)


@login_required
def achievements(request):
    """Trainer achievements view."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    # Get all unlocks for the trainer
    all_unlocks = trainer.unlocks.select_related('pokemon').all()
    
    # Count by type
    type_counts = {}
    for unlock in all_unlocks:
        ptype = unlock.pokemon.type
        type_counts[ptype] = type_counts.get(ptype, 0) + 1
    
    # Count total and shiny
    total_unlocked = all_unlocks.count()
    shiny_count = all_unlocks.filter(shiny=True).count()
    
    # Count by rarity
    rarity_counts = {}
    for unlock in all_unlocks:
        rarity = unlock.pokemon.rarity
        rarity_counts[rarity] = rarity_counts.get(rarity, 0) + 1
    
    # Badge sprite base URL from PokeAPI
    badge_base_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/badges"
    
    # Get team count
    team_count = trainer.team.members.count() if hasattr(trainer, 'team') else 0
    
    # Define achievements with PNG badges from PokeAPI
    achievements = [
        # Collection milestones
        {
            'id': 'collect_10',
            'name': 'Novice Collector',
            'description': 'Collect 10 different Pokémon',
            'requirement': 10,
            'current': total_unlocked,
            'badge_url': f'{badge_base_url}/1.png',
            'category': 'collection',
        },
        {
            'id': 'collect_25',
            'name': 'Rising Trainer',
            'description': 'Collect 25 different Pokémon',
            'requirement': 25,
            'current': total_unlocked,
            'badge_url': f'{badge_base_url}/6.png',
            'category': 'collection',
        },
        {
            'id': 'collect_50',
            'name': 'Skilled Trainer',
            'description': 'Collect 50 different Pokémon',
            'requirement': 50,
            'current': total_unlocked,
            'badge_url': f'{badge_base_url}/4.png',
            'category': 'collection',
        },
        {
            'id': 'collect_75',
            'name': 'Expert Collector',
            'description': 'Collect 75 different Pokémon',
            'requirement': 75,
            'current': total_unlocked,
            'badge_url': f'{badge_base_url}/3.png',
            'category': 'collection',
        },
        {
            'id': 'collect_100',
            'name': 'Master Collector',
            'description': 'Collect 100 different Pokémon',
            'requirement': 100,
            'current': total_unlocked,
            'badge_url': f'{badge_base_url}/2.png',
            'category': 'collection',
        },
        {
            'id': 'collect_150',
            'name': 'Pokemon Master',
            'description': 'Collect 150 different Pokémon',
            'requirement': 150,
            'current': total_unlocked,
            'badge_url': f'{badge_base_url}/9.png',
            'category': 'collection',
        },
        # Type-specific achievements
        {
            'id': 'fire_3',
            'name': 'Fire Beginner',
            'description': 'Collect 3 Fire-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Fire', 0),
            'badge_url': f'{badge_base_url}/20.png',
            'category': 'type',
        },
        {
            'id': 'fire_5',
            'name': 'Fire Champion',
            'description': 'Collect 5 Fire-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Fire', 0),
            'badge_url': f'{badge_base_url}/20.png',
            'category': 'type',
        },
        {
            'id': 'fire_10',
            'name': 'Fire Master',
            'description': 'Collect 10 Fire-type Pokémon',
            'requirement': 10,
            'current': type_counts.get('Fire', 0),
            'badge_url': f'{badge_base_url}/20.png',
            'category': 'type',
        },
        {
            'id': 'water_3',
            'name': 'Water Beginner',
            'description': 'Collect 3 Water-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Water', 0),
            'badge_url': f'{badge_base_url}/24.png',
            'category': 'type',
        },
        {
            'id': 'water_5',
            'name': 'Water Champion',
            'description': 'Collect 5 Water-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Water', 0),
            'badge_url': f'{badge_base_url}/24.png',
            'category': 'type',
        },
        {
            'id': 'water_10',
            'name': 'Water Master',
            'description': 'Collect 10 Water-type Pokémon',
            'requirement': 10,
            'current': type_counts.get('Water', 0),
            'badge_url': f'{badge_base_url}/24.png',
            'category': 'type',
        },
        {
            'id': 'grass_3',
            'name': 'Grass Beginner',
            'description': 'Collect 3 Grass-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Grass', 0),
            'badge_url': f'{badge_base_url}/26.png',
            'category': 'type',
        },
        {
            'id': 'grass_5',
            'name': 'Grass Champion',
            'description': 'Collect 5 Grass-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Grass', 0),
            'badge_url': f'{badge_base_url}/26.png',
            'category': 'type',
        },
        {
            'id': 'electric_3',
            'name': 'Electric Beginner',
            'description': 'Collect 3 Electric-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Electric', 0),
            'badge_url': f'{badge_base_url}/19.png',
            'category': 'type',
        },
        {
            'id': 'electric_5',
            'name': 'Electric Champion',
            'description': 'Collect 5 Electric-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Electric', 0),
            'badge_url': f'{badge_base_url}/19.png',
            'category': 'type',
        },
        {
            'id': 'psychic_3',
            'name': 'Psychic Beginner',
            'description': 'Collect 3 Psychic-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Psychic', 0),
            'badge_url': f'{badge_base_url}/23.png',
            'category': 'type',
        },
        {
            'id': 'psychic_5',
            'name': 'Psychic Champion',
            'description': 'Collect 5 Psychic-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Psychic', 0),
            'badge_url': f'{badge_base_url}/23.png',
            'category': 'type',
        },
        {
            'id': 'ghost_3',
            'name': 'Ghost Beginner',
            'description': 'Collect 3 Ghost-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Ghost', 0),
            'badge_url': f'{badge_base_url}/16.png',
            'category': 'type',
        },
        {
            'id': 'ghost_5',
            'name': 'Ghost Champion',
            'description': 'Collect 5 Ghost-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Ghost', 0),
            'badge_url': f'{badge_base_url}/16.png',
            'category': 'type',
        },
        {
            'id': 'dragon_3',
            'name': 'Dragon Beginner',
            'description': 'Collect 3 Dragon-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Dragon', 0),
            'badge_url': f'{badge_base_url}/16.png',
            'category': 'type',
        },
        {
            'id': 'dragon_5',
            'name': 'Dragon Champion',
            'description': 'Collect 5 Dragon-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Dragon', 0),
            'badge_url': f'{badge_base_url}/16.png',
            'category': 'type',
        },
        {
            'id': 'steel_3',
            'name': 'Steel Beginner',
            'description': 'Collect 3 Steel-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Steel', 0),
            'badge_url': f'{badge_base_url}/21.png',
            'category': 'type',
        },
        {
            'id': 'steel_5',
            'name': 'Steel Champion',
            'description': 'Collect 5 Steel-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Steel', 0),
            'badge_url': f'{badge_base_url}/21.png',
            'category': 'type',
        },
        {
            'id': 'fairy_3',
            'name': 'Fairy Beginner',
            'description': 'Collect 3 Fairy-type Pokémon',
            'requirement': 3,
            'current': type_counts.get('Fairy', 0),
            'badge_url': f'{badge_base_url}/29.png',
            'category': 'type',
        },
        {
            'id': 'fairy_5',
            'name': 'Fairy Champion',
            'description': 'Collect 5 Fairy-type Pokémon',
            'requirement': 5,
            'current': type_counts.get('Fairy', 0),
            'badge_url': f'{badge_base_url}/29.png',
            'category': 'type',
        },
        # Rarity achievements
        {
            'id': 'common_10',
            'name': 'Common Collector',
            'description': 'Collect 10 Common Pokémon',
            'requirement': 10,
            'current': rarity_counts.get('Common', 0),
            'badge_url': f'{badge_base_url}/1.png',
            'category': 'rarity',
        },
        {
            'id': 'uncommon_10',
            'name': 'Uncommon Hunter',
            'description': 'Collect 10 Uncommon Pokémon',
            'requirement': 10,
            'current': rarity_counts.get('Uncommon', 0),
            'badge_url': f'{badge_base_url}/1.png',
            'category': 'rarity',
        },
        {
            'id': 'rare_5',
            'name': 'Rare Finder',
            'description': 'Collect 5 Rare Pokémon',
            'requirement': 5,
            'current': rarity_counts.get('Rare', 0),
            'badge_url': f'{badge_base_url}/1.png',
            'category': 'rarity',
        },
        {
            'id': 'rare_10',
            'name': 'Rare Collector',
            'description': 'Collect 10 Rare Pokémon',
            'requirement': 10,
            'current': rarity_counts.get('Rare', 0),
            'badge_url': f'{badge_base_url}/5.png',
            'category': 'rarity',
        },
        {
            'id': 'epic_3',
            'name': 'Epic Seeker',
            'description': 'Collect 3 Epic Pokémon',
            'requirement': 3,
            'current': rarity_counts.get('Epic', 0),
            'badge_url': f'{badge_base_url}/5.png',
            'category': 'rarity',
        },
        {
            'id': 'epic_5',
            'name': 'Epic Collector',
            'description': 'Collect 5 Epic Pokémon',
            'requirement': 5,
            'current': rarity_counts.get('Epic', 0),
            'badge_url': f'{badge_base_url}/5.png',
            'category': 'rarity',
        },
        {
            'id': 'legendary_1',
            'name': 'Legendary Encounter',
            'description': 'Catch your first Legendary Pokémon',
            'requirement': 1,
            'current': rarity_counts.get('Legendary', 0),
            'badge_url': f'{badge_base_url}/8.png',
            'category': 'rarity',
        },
        {
            'id': 'legendary_3',
            'name': 'Legendary Hunter',
            'description': 'Catch 3 Legendary Pokémon',
            'requirement': 3,
            'current': rarity_counts.get('Legendary', 0),
            'badge_url': f'{badge_base_url}/7.png',
            'category': 'rarity',
        },
        {
            'id': 'legendary_5',
            'name': 'Legendary Master',
            'description': 'Catch 5 Legendary Pokémon',
            'requirement': 5,
            'current': rarity_counts.get('Legendary', 0),
            'badge_url': f'{badge_base_url}/7.png',
            'category': 'rarity',
        },
        # Shiny achievements
        {
            'id': 'shiny_1',
            'name': 'Shiny Discovery',
            'description': 'Catch your first Shiny Pokémon',
            'requirement': 1,
            'current': shiny_count,
            'badge_url': f'{badge_base_url}/2.png',
            'category': 'shiny',
        },
        {
            'id': 'shiny_3',
            'name': 'Shiny Seeker',
            'description': 'Catch 3 Shiny Pokémon',
            'requirement': 3,
            'current': shiny_count,
            'badge_url': f'{badge_base_url}/2.png',
            'category': 'shiny',
        },
        {
            'id': 'shiny_5',
            'name': 'Shiny Hunter',
            'description': 'Catch 5 Shiny Pokémon',
            'requirement': 5,
            'current': shiny_count,
            'badge_url': f'{badge_base_url}/3.png',
            'category': 'shiny',
        },
        {
            'id': 'shiny_10',
            'name': 'Shiny Master',
            'description': 'Catch 10 Shiny Pokémon',
            'requirement': 10,
            'current': shiny_count,
            'badge_url': f'{badge_base_url}/9.png',
            'category': 'shiny',
        },
        {
            'id': 'shiny_25',
            'name': 'Shiny Legend',
            'description': 'Catch 25 Shiny Pokémon',
            'requirement': 25,
            'current': shiny_count,
            'badge_url': f'{badge_base_url}/9.png',
            'category': 'shiny',
        },
        # Level achievements
        {
            'id': 'level_3',
            'name': 'Newcomer',
            'description': 'Reach Level 3',
            'requirement': 3,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/11.png',
            'category': 'level',
        },
        {
            'id': 'level_5',
            'name': 'Beginner Trainer',
            'description': 'Reach Level 5',
            'requirement': 5,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/11.png',
            'category': 'level',
        },
        {
            'id': 'level_10',
            'name': 'Rising Star',
            'description': 'Reach Level 10',
            'requirement': 10,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/13.png',
            'category': 'level',
        },
        {
            'id': 'level_15',
            'name': 'Advanced Trainer',
            'description': 'Reach Level 15',
            'requirement': 15,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/13.png',
            'category': 'level',
        },
        {
            'id': 'level_20',
            'name': 'Skilled Trainer',
            'description': 'Reach Level 20',
            'requirement': 20,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/14.png',
            'category': 'level',
        },
        {
            'id': 'level_25',
            'name': 'Veteran Trainer',
            'description': 'Reach Level 25',
            'requirement': 25,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/14.png',
            'category': 'level',
        },
        {
            'id': 'level_35',
            'name': 'Expert Trainer',
            'description': 'Reach Level 35',
            'requirement': 35,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/15.png',
            'category': 'level',
        },
        {
            'id': 'level_50',
            'name': 'Elite Trainer',
            'description': 'Reach Level 50',
            'requirement': 50,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/15.png',
            'category': 'level',
        },
        {
            'id': 'level_75',
            'name': 'Champion',
            'description': 'Reach Level 75',
            'requirement': 75,
            'current': trainer.level,
            'badge_url': f'{badge_base_url}/15.png',
            'category': 'level',
        },
        # Team achievements
        {
            'id': 'team_3',
            'name': 'Team Builder',
            'description': 'Have 3 Pokémon on your team',
            'requirement': 3,
            'current': team_count,
            'badge_url': f'{badge_base_url}/1.png',
            'category': 'team',
        },
        {
            'id': 'team_6',
            'name': 'Full Team',
            'description': 'Fill your team with 6 Pokémon',
            'requirement': 6,
            'current': team_count,
            'badge_url': f'{badge_base_url}/6.png',
            'category': 'team',
        },
    ]
    
    # Calculate unlocked count
    unlocked_count = sum(1 for a in achievements if a['current'] >= a['requirement'])
    
    context = {
        'trainer': trainer,
        'achievements': achievements,
        'unlocked_count': unlocked_count,
        'total_count': len(achievements),
    }
    return render(request, 'pokemon/achievements.html', context)


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

    # Get the trainer's team
    team = trainer.team

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
                'pokemon_sprite': pokemon.showdown_url,
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


@login_required
def admin_panel(request):
    """Admin panel for Lounelle to manage the game."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    # Check if user is Lounelle (admin)
    if trainer.user.username != 'Lounelle':
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('pokemon:dashboard')
    
    all_trainers = Trainer.objects.all().select_related('user')
    
    # Get shiny luck value (default is 1)
    shiny_luck = getattr(trainer, 'shiny_luck', 1)
    
    context = {
        'trainer': trainer,
        'all_trainers': all_trainers,
        'shiny_luck': shiny_luck,
    }
    return render(request, 'pokemon/admin_panel.html', context)


@login_required
def admin_give_eggs(request):
    """Admin: Give eggs to all trainers."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    if trainer.user.username != 'Lounelle':
        messages.error(request, 'You do not have permission to do this.')
        return redirect('pokemon:dashboard')
    
    if request.method == 'POST':
        egg_count = int(request.POST.get('egg_count', 1))
        
        # Give to all trainers
        all_trainers = Trainer.objects.all()
        for t in all_trainers:
            t.egg_count += egg_count
            t.save()
        messages.success(request, f'Gave {egg_count} egg(s) to all trainers.')
    
    return redirect('pokemon:admin_panel')


@login_required
def admin_give_pokeballs(request):
    """Admin: Give pokeballs to all trainers."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    if trainer.user.username != 'Lounelle':
        messages.error(request, 'You do not have permission to do this.')
        return redirect('pokemon:dashboard')
    
    if request.method == 'POST':
        pokeball_count = int(request.POST.get('pokeball_count', 10))
        
        # Give to all trainers
        all_trainers = Trainer.objects.all()
        for t in all_trainers:
            t.pokeball_count += pokeball_count
            t.save()
        messages.success(request, f'Gave {pokeball_count} pokeball(s) to all trainers.')
    
    return redirect('pokemon:admin_panel')


@login_required
def admin_give_coins(request):
    """Admin: Give PokeHunt Coins to all trainers."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    if trainer.user.username != 'Lounelle':
        messages.error(request, 'You do not have permission to do this.')
        return redirect('pokemon:dashboard')
    
    if request.method == 'POST':
        coin_count = int(request.POST.get('coin_count', 100))
        
        # Give to all trainers
        all_trainers = Trainer.objects.all()
        for t in all_trainers:
            t.hunt_coins += coin_count
            t.save()
        messages.success(request, f'Gave {coin_count} PokeHunt Coins to all trainers.')
    
    return redirect('pokemon:admin_panel')


@login_required
def admin_toggle_shiny(request):
    """Admin: Toggle shiny status for a trainer's pokemon."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    if trainer.user.username != 'Lounelle':
        messages.error(request, 'You do not have permission to do this.')
        return redirect('pokemon:dashboard')
    
    if request.method == 'POST':
        # Toggle global shiny luck (100% shiny mode)
        current_shiny_luck = getattr(trainer, 'shiny_luck', 1)
        if current_shiny_luck >= 100:
            trainer.shiny_luck = 1
            messages.success(request, 'Disabled 100% Shiny mode.')
        else:
            trainer.shiny_luck = 100
            messages.success(request, 'Enabled 100% Shiny mode! All hatched/caught Pokemon will be shiny!')
        trainer.save()
    
    return redirect('pokemon:admin_panel')


@login_required
def shop(request):
    """Shop view for purchasing items with Hunt Coins."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    team = trainer.team
    
    # Get all active shop items
    shop_items = ShopItem.objects.filter(is_active=True)
    
    context = {
        'trainer': trainer,
        'team_size': team.members.count(),
        'max_team_size': trainer.max_team_size,
        'shop_items': shop_items,
    }
    return render(request, 'pokemon/shop.html', context)


@login_required
def inventory(request):
    """Inventory view showing user's owned items."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    filter_category = request.GET.get('category', 'all')
    inventory_items = trainer.inventory.all()
    
    if filter_category != 'all':
        inventory_items = inventory_items.filter(category=filter_category)
    
    category_counts = {
        'all': trainer.inventory.count(),
        'pokeball': trainer.inventory.filter(category='pokeball').count(),
        'berry': trainer.inventory.filter(category='berry').count(),
        'potion': trainer.inventory.filter(category='potion').count(),
        'status_heal': trainer.inventory.filter(category='status_heal').count(),
        'evolution': trainer.inventory.filter(category='evolution').count(),
        'vitamin': trainer.inventory.filter(category='vitamin').count(),
        'exp': trainer.inventory.filter(category='exp').count(),
        'egg': trainer.inventory.filter(category='egg').count(),
    }
    
    context = {
        'trainer': trainer,
        'team_size': trainer.team.members.count(),
        'max_team_size': trainer.max_team_size,
        'inventory_items': inventory_items,
        'filter_category': filter_category,
        'category_counts': category_counts,
    }
    return render(request, 'pokemon/inventory.html', context)
