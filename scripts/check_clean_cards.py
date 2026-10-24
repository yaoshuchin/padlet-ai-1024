import json

with open('board_clean.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for c_idx, col in enumerate(d['columns']):
    print(f"\n--- Col {c_idx+1}: {col['title']} ({len(col['cards'])} cards) ---")
    for card in col['cards']:
        print(f"  [{card['color_label']}] Title: {card['title'] or '(無標題)'}")
        if card['body']:
            print(f"      Body: {card['body'][:80]}...")
        if card['link']:
            print(f"      Link: {card['link'][:80]}")
        if card['image']:
            print(f"      Image: {card['image'][:80]}")
