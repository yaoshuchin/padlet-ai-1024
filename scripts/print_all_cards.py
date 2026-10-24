import json

with open('padlet_full_data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for s_idx, s in enumerate(d['sections']):
    print(f"\n=================== SECTION {s_idx+1}: {s['title']} ({s['cards_count']} cards) ===================")
    for c_idx, c in enumerate(s['cards']):
        print(f"[{c_idx+1}] ID: {c['id']} | Color: {c['color']} ({c['raw_color']})")
        print(f"     Title: {c['title']}")
        if c['body']:
            print(f"     Body: {repr(c['body'][:120])}")
        if c['link']:
            print(f"     Link: {c['link']}")
        if c['image']:
            print(f"     Image: {c['image'][:80]}...")
