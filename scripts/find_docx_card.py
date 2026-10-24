with open('data/padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('4113216291')
if idx != -1:
    print("Found 4113216291:")
    print(html[idx-100:idx+800])
else:
    print("Not found by ID, searching by 範例教案")
    idx2 = html.find('範例教案')
    if idx2 != -1:
        print("Found 範例教案:")
        print(html[idx2-100:idx2+800])
