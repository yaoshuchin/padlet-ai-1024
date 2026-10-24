import json
import re

with open('data/board.json', 'r', encoding='utf-8') as f:
    board = json.load(f)

with open('data/padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    html = f.read()

# All image URLs in board
img_urls = set()
if board.get('background'):
    img_urls.add(board['background'])

for col in board.get('columns', []):
    for card in col.get('cards', []):
        if card.get('image'):
            img_urls.add(card['image'])

# Also any image tags in html
for m in re.findall(r'src=\"(https://v1\.padlet\.pics/[^\"]+)\"', html):
    img_urls.add(m.replace('&amp;', '&'))

for m in re.findall(r'src=\"(https://padlet-uploads-usc1\.storage\.googleapis\.com/[^\"]+)\"', html):
    img_urls.add(m.replace('&amp;', '&'))

print(f"Total unique images to download: {len(img_urls)}")
with open('data/all_image_urls.txt', 'w', encoding='utf-8') as out:
    for u in sorted(img_urls):
        out.write(u + '\n')

print("Saved data/all_image_urls.txt")
