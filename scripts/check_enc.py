with open('padlet_dump.html', 'rb') as f:
    raw = f.read()

# Let's inspect encoding
import re

for enc in ['utf-8', 'cp950', 'gbk', 'utf-16']:
    try:
        t = raw.decode(enc)
        print(f"Decoded with {enc}")
        m = re.search(r'"name":"([^"]+)"', t)
        if m:
            print("Name:", m.group(1))
        m2 = re.search(r'"description":"([^"]+)"', t)
        if m2:
            print("Description:", m2.group(1))
        break
    except Exception as e:
        print(f"Failed {enc}: {e}")
