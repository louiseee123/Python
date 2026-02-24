# Update dashboard view to include shiny status for team members

with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Update the dashboard view context to include shiny status
old_context = '''    context = {
        'trainer': trainer,
        'team': team,
        'team_members': members,
        'daily_tasks': daily_tasks,
        'completed_tasks': completed_task_ids,
        'unlocked_count': trainer.unlocks.count(),
        'total_pokemon': total_pokemon,
    }'''

new_context = '''    # Get shiny status for team members
    team_shiny = {}
    for member in members:
        unlock = trainer.unlocks.filter(pokemon=member.pokemon).first()
        member.shiny = unlock.shiny if unlock else False
    
    context = {
        'trainer': trainer,
        'team': team,
        'team_members': members,
        'daily_tasks': daily_tasks,
        'completed_tasks': completed_task_ids,
        'unlocked_count': trainer.unlocks.count(),
        'total_pokemon': total_pokemon,
    }'''

content = content.replace(old_context, new_context)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('dashboard view updated with shiny status!')
