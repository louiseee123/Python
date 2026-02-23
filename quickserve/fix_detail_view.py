# Fix the pokemon_detail view to add team variable

views_content = '''from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from datetime import date
import random
from .models import Trainer, Pokemon, Team, TeamMember, PokemonUnlock, DailyTask, TrainerTaskCompletion


def home(request):
    """Landing page - redirects to appropriate page based on auth status."""
    if request.user.is_authenticated:
        # Check if user has a trainer profile
        try:
            trainer = request.user.trainer
            # If no team, redirect to starter selection
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
        # Create trainer and redirect to starter selection
        trainer = Trainer.objects.create(
            user=request.user,
            level=1,
            experience=0,
            max_team_size=6
        )
        Team.objects.create(trainer=trainer)
        
        # Unlock starter Pokemon for this trainer
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
    
    # Check if already selected starter
    team = trainer.team
    if team.members.count() > 0:
        return redirect('pokemon:dashboard')
    
    starters = Pokemon.objects.filter(is_starter=True)
    
    if request.method == 'POST':
        pokemon_id = request.POST.get('pokemon_id')
        pokemon = get_object_or_404(Pokemon, id=pokemon_id, is_starter=True)
        
        # Check if already unlocked
        unlock, created = PokemonUnlock.objects.get_or_create(
            trainer=trainer,
            pokemon=pokemon
        )
        
        # Add to team
        TeamMember.objects.create(
            team=team,
            pokemon=pokemon,
            nickname=pokemon.name
        )
        
        # Add XP for selecting starter
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
    team_members = team.members.all()[:3]  # First 3 for preview
    
    # Get unlocked Pokemon count
    unlocked_count = trainer.unlocks.count()
    total_pokemon = Pokemon.objects.count()
    
    # Get daily tasks
    today = date.today()
    daily_tasks = DailyTask.objects.filter(is_active=True)
    
    # Check which tasks are completed
    completed_tasks = TrainerTaskCompletion.objects.filter(
        trainer=trainer,
        date=today
    ).values_list('task_id', flat=True)
    
    # Mark login task as completed automatically if not already
    login_task = DailyTask.objects.filter(task_type='login').first()
    if login_task and login_task.id not in completed_tasks:
        # Complete the login task
        TrainerTaskCompletion.objects.get_or_create(
            trainer=trainer,
            task=login_task,
            date=today
        )
        # Add XP and eggs for login task
        trainer.add_xp(login_task.xp_reward)
        if login_task.egg_reward > 0:
            trainer.egg_count += login_task.egg_reward
            trainer.save()
        completed_tasks = list(completed_tasks) + [login_task.id]
    
    context = {
        'trainer': trainer,
        'team_members': team_members,
        'unlocked_count': unlocked_count,
        'total_pokemon': total_pokemon,
        'daily_tasks': daily_tasks,
        'completed_tasks': completed_tasks,
    }
    return render(request, 'pokemon/dashboard.html', context)


@login_required
def pokedex(request):
    """Pokédex view showing all Pokemon with lock/unlock status."""
    try:
        trainer = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('pokemon:create_trainer')
    
    # Get filter parameters
    pokemon_type = request.GET.get('type')
    search_query = request.GET.get('search')
    
    # Get all unlocked Pokemon IDs and their shiny status
    unlocked_data = {}  # {pokemon_id: is_shiny}
    for unlock in trainer.unlocks.all():
        unlocked_data[unlock.pokemon_id] = unlock.shiny
    
    # Get all Pokemon
    pokemon_list = Pokemon.objects.all()
    
    # Apply filters
    if pokemon_type:
        pokemon_list = pokemon_list.filter(type=pokemon_type)
    if search_query:
        pokemon_list = pokemon_list.filter(name__icontains=search_query)
    
    # Get all types for filter buttons
    types = Pokemon.TYPES
    
    # Get team pokemon ids
    team_pokemon_ids = set(trainer.team.members.values_list('pokemon_id', flat=True))
    
    context = {
        'pokemon_list': pokemon_list,
        'unlocked_ids': set(unlocked_data.keys()),
        'unlocked_data': unlocked_data,
        'types': types,
        'selected_type': pokemon_type,
        'search_query': search_query,
        'trainer': trainer,
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
    
    # Get unlocked Pokemon that are not in team (with shiny status)
    unlocked_pokemon = trainer.unlocks.select_related('pokemon')
    team_pokemon_ids = team.members.values_list('pokemon_id', flat=True)
    available_pokemon = []  # List of (pokemon, shiny) tuples
    for u in unlocked_pokemon:
        if u.pokemon.id not in team_pokemon_ids:
            available_pokemon.append((u.pokemon, u.shiny))
    
    # Get shiny status for team members
    team_shiny = {}  # {member_id: is_shiny}
    for member in members:
        unlock = trainer.unlocks.filter(pokemon=member.pokemon).first()
        team_shiny[member.id] = unlock.shiny if unlock else False
    
    context = {
        'trainer': trainer,
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
    
    # Check if team is full
    if team.is_full:
        messages.error(request, f'Your team is full! Max size: {trainer.max_team_size}')
        return redirect('pokemon:pokedex')
    
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    
    # Remove level unlock requirement - all Pokemon can be added
    # (keeping unlock check for consistency but will auto-unlock if needed)
    if not trainer.unlocks.filter(pokemon=pokemon).exists():
        PokemonUnlock.objects.get_or_create(trainer=trainer, pokemon=pokemon)
    
    # Check if already in team
    if team.members.filter(pokemon=pokemon).exists():
        messages.error(request, 'This Pokemon is already in your team!')
        return redirect('pokemon:my_team')
    
    # Add to team
    TeamMember.objects.create(
        team=team,
        pokemon=pokemon,
        nickname=pokemon.name
    )
    
    # Check for team building task
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
    
    # Check if already completed
    if TrainerTaskCompletion.objects.filter(trainer=trainer, task=task, date=today).exists():
        messages.error(request, 'Task already completed!')
        return redirect('pokemon:dashboard')
    
    # Complete the task
    TrainerTaskCompletion.objects.create(trainer=trainer, task=task, date=today)
    trainer.add_xp(task.xp_reward)
    
    # Award egg reward if any
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
    
    # Get the Pokemon
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    
    # Get team
    team = trainer.team
    
    # Check if unlocked
    unlock = trainer.unlocks.filter(pokemon=pokemon).first()
    is_unlocked = unlock is not None
    is_shiny = unlock.shiny if unlock else False
    
    # Get all unlock instances for this trainer (to handle duplicates)
    all_unlocks = trainer.unlocks.filter(pokemon=pokemon)
    
    # Check if in team
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
    
    # Check if trainer has eggs
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
    
    # Check if already unlocked (for non-shiny)
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
        unlock.save()
    
    # Decrease egg count
    trainer.egg_count -= 1
    trainer.save()
    
    # Add XP for hatching (bonus based on rarity)
    xp_bonus = {'Common': 5, 'Uncommon': 10, 'Rare': 15, 'Epic': 25, 'Legendary': 50}
    trainer.add_xp(xp_bonus.get(selected_rarity, 10))
    
    # Check if team is not full, add to team
    team = trainer.team
    added_to_team = False
    if not team.is_full:
        # Check if already in team
        if not team.members.filter(pokemon=random_pokemon).exists():
            TeamMember.objects.create(
                team=team,
                pokemon=random_pokemon,
                nickname=random_pokemon.name
            )
            added_to_team = True
    
    # Get XP earned
    xp_earned = xp_bonus.get(selected_rarity, 10)
    
    # Extra XP for shiny Pokemon
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
    
    # Get recent activity (unlocks)
    recent_unlocks = trainer.unlocks.select_related('pokemon').order_by('-unlocked_at')[:5]
    
    context = {
        'trainer': trainer,
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
        
        # Create user
        user = User.objects.create_user(username=username, password=password)
        
        # Create trainer profile
        trainer = Trainer.objects.create(
            user=user,
            level=1,
            experience=0,
            max_team_size=6
        )
        Team.objects.create(trainer=trainer)
        
        # Unlock starter Pokemon
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
'''

with open('quickserve/pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(views_content)

print('Fixed views.py with team variable!')
