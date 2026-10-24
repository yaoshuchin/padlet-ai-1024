import json

with open('padlet_full_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

with open('padlet_data.json', 'r', encoding='utf-8') as f:
    feed = json.load(f)

feed_map = {}
for it in feed['items']:
    guid = it.get('guid', '')
    cid = guid.split('/')[-1] if '/' in guid else ''
    feed_map[cid] = it

lines = []
for s_idx, s in enumerate(d['sections']):
    lines.append(f"SECTION {s_idx+1}: {s['title']} ({len(s['cards'])} cards)")
    for c in s['cards']:
        cid = c['id']
        f_it = feed_map.get(cid, {})
        title = c['title'] or f_it.get('title', '')
        desc = f_it.get('description', '') or c['body']
        link = c['link'] or (f_it.get('enclosures', [{}])[0].get('url') if f_it.get('enclosures') else '')
        lines.append(f"  - [{c['color']}] ID={cid} | Title='{title}' | Link='{link}' | HasDesc={bool(desc)}")
        if desc and len(desc) < 150:
            lines.append(f"      Desc: {desc}")
    lines.append("")

with open('clean_cards_list.txt', 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))

print("Saved clean_cards_list.txt")
