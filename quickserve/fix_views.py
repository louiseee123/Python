# Script to update views.py to use the new template
with open('pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the template path
old_line = "return render(request, 'pokemon/my_team.html', context)"
new_line = "return render(request, 'pokemon/my_team_updated.html', context)"

content = content.replace(old_line, new_line)

with open('pokemon/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Updated views.py to use my_team_updated.html")
