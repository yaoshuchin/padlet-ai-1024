with open('padlet_rendered.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find("說在前面")
print("Before:")
print(html[idx-300:idx])
print("After:")
print(html[idx:idx+1500])
