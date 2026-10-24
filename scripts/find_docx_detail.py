with open('data/padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('4113216291')
with open('data/docx_card_detail.txt', 'w', encoding='utf-8') as out:
    out.write(html[idx:idx+3500])

print("Wrote docx_card_detail.txt")
