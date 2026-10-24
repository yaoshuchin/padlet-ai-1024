import re
from bs4 import BeautifulSoup

with open('padlet_rendered.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

print("All elements with scroll or overflow in style or class:")
for el in soup.find_all(attrs={'class': lambda c: c and ('overflow' in c or 'scroll' in c)}):
    print(el.name, el.get('id'), el.get('class')[:5])
