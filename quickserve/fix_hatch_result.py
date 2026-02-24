# Fix hatch_result.html by adding CSS classes for rarity

with open('pokemon/templates/pokemon/hatch_result.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''            <div class="rarity-badge" style="background: linear-gradient(135deg, #{{rarity_color}}, #{{rarity_color_dark}}); padding: 8px 16px; border-radius: 15px; margin-bottom: 15px; font-weight: bold;">
                {{ rarity }}
            </div>'''

new = '''            <div class="rarity-badge rarity-{{ rarity|lower }}">
                {{ rarity }}
            </div>'''

content = content.replace(old, new)

# Add rarity CSS classes before </style>
css_addition = '''
        .rarity-badge {
            padding: 8px 16px;
            border-radius: 15px;
            margin-bottom: 15px;
            font-weight: bold;
            display: inline-block;
        }
        .rarity-common { background: linear-gradient(135deg, #95a5a6, #7f8c8d); color: white; }
        .rarity-uncommon { background: linear-gradient(135deg, #2ecc71, #27ae60); color: white; }
        .rarity-rare { background: linear-gradient(135deg, #3498db, #2980b9); color: white; }
        .rarity-epic { background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; }
        .rarity-legendary { background: linear-gradient(135deg, #f1c40f, #f39c12); color: #1a1a2e; }

'''

content = content.replace('        .added-to-team {', css_addition + '        .added-to-team {')

with open('pokemon/templates/pokemon/hatch_result.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
