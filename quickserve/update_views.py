import re

# Read the views.py file
with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()


# Update claim_task_xp function
old_claim_task = '''@login_required
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
    
    return redirect('pokemon:dashboard')'''

new_claim_task = '''@login_required
def claim_task_xp(request, task_id):
    """Claim XP, eggs, and coins for completing a task - returns JSON for modal."""
    task = get_object_or_404(DailyTask, id=task_id)
    trainer = request.user.trainer
    today = date.today()
    
    if TrainerTaskCompletion.objects.filter(trainer=trainer, task=task, date=today).exists():
        return JsonResponse({
            'success': False,
            'error': 'Task already completed today!'
        })
    
    # Create completion record
    TrainerTaskCompletion.objects.create(trainer=trainer, task=task, date=today)
    
    # Apply rewards
    trainer.add_xp(task.xp_reward)
    
    rewards = {
        'xp': task.xp_reward,
        'eggs': 0,
        'coins': 0
    }
    
    if task.egg_reward > 0:
        trainer.egg_count += task.egg_reward
        rewards['eggs'] = task.egg_reward
    
    if task.coin_reward > 0:
        trainer.hunt_coins += task.coin_reward
        rewards['coins'] = task.coin_reward
    
    trainer.save()
    
    return JsonResponse({
        'success': True,
        'task_name': task.name,
        'rewards': rewards,
        'new_egg_count': trainer.egg_count,
        'new_coin_count': trainer.hunt_coins,
        'new_level': trainer.level,
        'new_xp': trainer.experience,
        'xp_for_next': trainer.xp_for_next_level
    })'''

content = content.replace(old_claim_task, new_claim_task)

# Update add_to_team to redirect to dashboard instead of my_team
content = content.replace("return redirect('pokemon:my_team')", "return redirect('pokemon:dashboard')")

# Update rename_member to redirect to dashboard
content = content.replace("return redirect('pokemon:my_team')", "return redirect('pokemon:dashboard')")

# Update remove_from_team to redirect to dashboard
content = content.replace("return redirect('pokemon:my_team')", "return redirect('pokemon:dashboard')")

# Update add_to_team to handle coin rewards
old_add_team = '''    add_team_task = DailyTask.objects.filter(task_type='add_team').first()
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
        messages.success(request, f'Added {pokemon.name} to team!')'''

new_add_team = '''    add_team_task = DailyTask.objects.filter(task_type='add_team').first()
    if add_team_task:
        today = date.today()
        if not TrainerTaskCompletion.objects.filter(trainer=trainer, task=add_team_task, date=today).exists():
            TrainerTaskCompletion.objects.create(trainer=trainer, task=add_team_task, date=today)
            trainer.add_xp(add_team_task.xp_reward)
            if add_team_task.egg_reward > 0:
                trainer.egg_count += add_team_task.egg_reward
            if add_team_task.coin_reward > 0:
                trainer.hunt_coins += add_team_task.coin_reward
            trainer.save()
            messages.success(request, f'Added {pokemon.name} to team! +{add_team_task.xp_reward} XP, +{add_team_task.egg_reward} Egg(s), +{add_team_task.coin_reward} Coins')
        else:
            messages.success(request, f'Added {pokemon.name} to team!')
    else:
        messages.success(request, f'Added {pokemon.name} to team!')'''

content = content.replace(old_add_team, new_add_team)

# Update dashboard to show all team members and handle coin rewards for login
old_dashboard = '''    team_members = team.members.all()[:3]'''
new_dashboard = '''    team_members = team.members.all()[:6]  # Show all team members'''
content = content.replace(old_dashboard, new_dashboard)

# Update login task to handle coin rewards
old_login = '''    if login_task and login_task.id not in completed_tasks:
        TrainerTaskCompletion.objects.get_or_create(
            trainer=trainer,
            task=login_task,
            date=today
        )
        trainer.add_xp(login_task.xp_reward)
        if login_task.egg_reward > 0:
            trainer.egg_count += login_task.egg_reward
            trainer.save()
        completed_tasks = list(completed_tasks) + [login_task.id]'''

new_login = '''    if login_task and login_task.id not in completed_tasks:
        TrainerTaskCompletion.objects.get_or_create(
            trainer=trainer,
            task=login_task,
            date=today
        )
        trainer.add_xp(login_task.xp_reward)
        if login_task.egg_reward > 0:
            trainer.egg_count += login_task.egg_reward
        if login_task.coin_reward > 0:
            trainer.hunt_coins += login_task.coin_reward
        trainer.save()
        completed_tasks = list(completed_tasks) + [login_task.id]'''

content = content.replace(old_login, new_login)

# Write the updated content
with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)


print("Views updated successfully!")
