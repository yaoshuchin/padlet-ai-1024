import json

with open('padlet_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

lines = []
lines.append(f"Title: {data['title']}")
lines.append(f"Description: {data['description']}")
lines.append(f"Total items: {len(data['items'])}\n")

for idx, item in enumerate(data['items']):
    title = item.get('title', '')
    desc = item.get('description', '')
    enclosures = item.get('enclosures', [])
    urls = [e.get('url', '') for e in enclosures if e.get('url')]
    
    lines.append(f"[{idx+1}] Title: {title}")
    if desc:
        lines.append(f"     Desc: {desc}")
    if urls:
        lines.append(f"     Attachments: {urls}")
    lines.append("")

with open('feed_summary.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("Successfully written to feed_summary.txt")
