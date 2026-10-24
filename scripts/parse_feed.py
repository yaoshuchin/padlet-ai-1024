import xml.etree.ElementTree as ET

tree = ET.parse('feed.xml')
root = tree.getroot()

channel = root.find('channel')
title = channel.find('title').text if channel.find('title') is not None else ''
desc = channel.find('description').text if channel.find('description') is not None else ''

print(f"Title: {title}")
print(f"Description: {desc}")

items = channel.findall('item')
print(f"Total items: {len(items)}")

for idx, item in enumerate(items):
    ititle = item.find('title').text if item.find('title') is not None else ''
    idesc = item.find('description').text if item.find('description') is not None else ''
    ilink = item.find('link').text if item.find('link') is not None else ''
    author = item.find('author').text if item.find('author') is not None else ''
    pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''
    category = item.find('category').text if item.find('category') is not None else ''
    print(f"\n--- Item {idx+1} ---")
    print(f"Title: {ititle}")
    print(f"Author: {author}")
    print(f"Category: {category}")
    print(f"Link: {ilink}")
    print(f"Desc snippet: {idesc[:100]}...")
