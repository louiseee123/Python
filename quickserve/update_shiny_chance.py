import os
import re

# Read the views.py file
with open('quickserve/pokemon/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the shiny check
old_code = "    # Check for shiny (1% chance)\n    is_shiny = random.randint(1, 100) == 1"
new_code = "    # Check for shiny using trainer's shiny_luck (default 1%)\n    shiny_chance = getattr(trainer, 'shiny_luck', 1)\n    is_shiny = random.randint(1, 100) <= shiny_chance"

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('quickserve/pokemon/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated views.py with shiny_luck support!")
else:
    print("Could not find the exact code to replace. Current code might be different.")
    # Try to find a similar pattern
    pattern = r"is_shiny = random\.randint\(1, 100\) == 1"
    if re.search(pattern, content):
        content = re.sub(pattern, "shiny_chance = getattr(trainer, 'shiny_luck', 1)\n    is_shiny = random.randint(1, 100) <= shiny_chance", content)
        with open('quickserve/pokemon/views.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Updated using regex pattern matching!")
    else:
        print("Pattern not found. Let me show what's around 'is_shiny':")
        # Find and show context
        match = re.search(r'is_shiny.*', content)
        if match:
            print(f"Found: {match.group()}")
