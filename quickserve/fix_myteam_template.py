# Fix my_team.html to load template tags

with open('pokemon/templates/pokemon/my_team.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '{% load static %}'
new = '{% load static %}\n{% load pokextras %}'

content = content.replace(old, new)

with open('pokemon/templates/pokemon/my_team.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('my_team template fixed')
