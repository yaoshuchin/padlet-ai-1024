import re
from bs4 import BeautifulSoup

with open('data/padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Look for docx or .zip or wish 4113216291
matches = re.findall(r'https://[^\s"\'<>]+(?:docx|\.pdf|\.zip|expiry_token|download)[^\s"\'<>]*', html)
print(f"Found {len(matches)} matches in padlet_ultrawide.html:")
for m in set(matches):
    print(" -", m[:120])
