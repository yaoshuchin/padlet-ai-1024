import re

with open('padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    html = f.read()

body_match = re.search(r'<body[^>]*style="([^"]*)"', html)
if body_match:
    print("Body style:", body_match.group(1))

# look for wallpaper
wp = re.findall(r'https://[^"]*wallpaper[^"]*', html)
print("Wallpapers:", wp)

pics = re.findall(r'https://v1\.padlet\.pics/[^"\')\s]+', html)
print("Padlet pics:", set(pics))
