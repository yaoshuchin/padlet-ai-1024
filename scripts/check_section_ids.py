import json
import re
from bs4 import BeautifulSoup

with open('padlet_rendered.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Find all cards across the DOM
all_cards = soup.find_all(attrs={'data-section-id': True})
print(f"Cards with data-section-id: {len(all_cards)}")

# Find all section headers and their section IDs
# Look at button or div with section id: id="section-action-menu-button-399452156" or data-id="399452156"
sections_map = {}
for el in soup.find_all(attrs={'data-testid': 'sectionTitleText'}):
    sec_title = el.get_text().strip()
    # Find closest section id in parent or siblings
    parent = el.parent
    sec_id = None
    for _ in range(10):
        if not parent:
            break
        # Check id
        for child in parent.find_all(attrs={'id': re.compile(r'section-action-menu-button-(\d+)')}):
            m = re.search(r'section-action-menu-button-(\d+)', child['id'])
            if m:
                sec_id = m.group(1)
                break
        if sec_id:
            break
        if parent.get('data-id'):
            sec_id = parent['data-id']
            break
        parent = parent.parent
    
    if sec_id:
        sections_map[sec_id] = sec_title

print(f"Found {len(sections_map)} sections with IDs:")
for sid, stitle in sections_map.items():
    print(f"  ID: {sid} -> {stitle}")

# Let's count cards per section ID
cards_by_sec = {}
for c in all_cards:
    sid = c['data-section-id']
    cards_by_sec.setdefault(sid, []).append(c)

print("\nCards grouped by section ID:")
for sid, clist in cards_by_sec.items():
    sec_name = sections_map.get(sid, 'UNKNOWN')
    print(f"  Section {sid} ({sec_name}): {len(clist)} cards")
