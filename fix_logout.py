import os

# Read the file
file_path = r"c:\Users\Windows 10 Pro\Documents\EDP\Python\quickserve\pokemon\templates\pokemon\dashboard.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the function definition
content = content.replace(
    'function showLogoutModal() {',
    'function showLogoutModal(e) { if (e) { e.preventDefault(); e.stopPropagation(); }'
)

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("File updated successfully!")
