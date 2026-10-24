import json

with open('padlet_full_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = []
lines.append(f"Board: {data['title']}")
lines.append(f"Description: {data['description']}")
lines.append(f"Author: {data['author']}")
lines.append(f"Total Sections: {data['total_sections']}")
lines.append(f"Total Cards: {data['total_cards']}\n")

for s in data['sections']:
    lines.append(f"=== [ {s['title']} ] (Color: {s['color']}, Cards: {s['cards_count']}) ===")
    for c in s['cards']:
        lines.append(f"  * [{c['color']}] {c['title'] or '(無標題)'}")
        if c['body']:
            lines.append(f"    內文: {c['body'][:60]}...")
        if c['link']:
            lines.append(f"    連結: {c['link']}")
        if c['image']:
            lines.append(f"    圖片: {c['image'][:60]}...")
    lines.append("")

with open('board_overview.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Wrote board_overview.txt successfully!")
