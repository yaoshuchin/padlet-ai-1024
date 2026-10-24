import xml.etree.ElementTree as ET
import json
import re

tree = ET.parse('feed.xml')
root = tree.getroot()
channel = root.find('channel')

title = channel.findtext('title') or ''
desc = channel.findtext('description') or ''

items = []
for item in channel.findall('item'):
    ititle = item.findtext('title') or ''
    idesc = item.findtext('description') or ''
    ilink = item.findtext('link') or ''
    iauthor = item.findtext('author') or ''
    ipubDate = item.findtext('pubDate') or ''
    guid = item.findtext('guid') or ''
    
    # check if there are enclosures or media or categories
    categories = [c.text for c in item.findall('category') if c.text]
    enclosures = [e.attrib for e in item.findall('enclosure')]
    
    items.append({
        'title': ititle,
        'description': idesc,
        'link': ilink,
        'author': iauthor,
        'pubDate': ipubDate,
        'guid': guid,
        'categories': categories,
        'enclosures': enclosures
    })

data = {
    'title': title,
    'description': desc,
    'total_items': len(items),
    'items': items
}

with open('padlet_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(items)} items to padlet_data.json")
