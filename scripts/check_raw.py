# Let's inspect the actual raw bytes of "Name"
with open('padlet_dump.html', 'rb') as f:
    raw = f.read()

import re
idx = raw.find(b'"name":"')
if idx != -1:
    print("Raw bytes of name:", raw[idx:idx+50])
