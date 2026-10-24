import re

with open('padlet_rendered.html', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

print('Length:', len(c))
headers = re.findall(r'<h[1-6][^>]*>(.*?)</h[1-6]>', c)
print('Headers count:', len(headers))
for h in headers[:20]:
    print(' - Header:', h[:80])

# Look for section titles or column titles
# Often in buttons or span or h2
spans = re.findall(r'<span[^>]*>(.*?)</span>', c)
print(f'Total spans: {len(spans)}')
# Let's see some distinctive spans
for s in spans:
    if any(k in s for k in ['工作流', '範例', '工具', '實作', '資料', '準備', '第一', '第二', '第三']):
        print('  Span match:', s[:100])
