import json

with open('data/padlet_data.json', 'r', encoding='utf-8') as f:
    feed = json.load(f)

print(f"Total feed items: {len(feed['items'])}")
files_to_download = []
for idx, item in enumerate(feed['items']):
    title = item.get('title', '')
    encs = item.get('enclosures', [])
    for e in encs:
        u = e.get('url')
        if u:
            files_to_download.append((title, u))
            print(f"[{idx+1}] Title: {title} | URL: {u}")

print(f"\nTotal files from feed: {len(files_to_download)}")
