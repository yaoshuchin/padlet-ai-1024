import json

with open('data/board.json', 'r', encoding='utf-8') as f:
    board = json.load(f)

for col in board['columns']:
    for card in col['cards']:
        link = card.get('link', '')
        att_type = card.get('attachment_type', '')
        if att_type in ['archive', 'pdf', 'doc', 'image'] or any(ext in link.lower() for ext in ['.zip', '.pdf', '.docx', '.txt', '.png', '.jpg', 'download=1']):
            print(f"[{col['title']}] '{card['title']}' -> Link: {link}")
