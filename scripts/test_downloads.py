import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

test_urls = [
    ("zip1", "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/df8935d96eef982d28dcd34543dd5999/tw_spark_edu_lesson_pack_generator.zip"),
    ("docx", "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/094571458e1d9ef6a1851ec6eb3fcea2/____.docx"),
    ("pdf", "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/97bd14ec22dd012ab4adec5b91765598/10_____5_____07_____.pdf"),
    ("txt", "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/bec83d0808db2b5921330a89184b4560/Gem__.txt"),
    ("thumb", "https://v1.padlet.pics/1/image.webp?t=c_limit%2Cdpr_1%2Ch_277%2Cw_500&url=https%3A%2F%2Fpadlet-uploads-usc1.storage.googleapis.com%2F1736270122%2F28b7d5b598f43dd3f037bd9888905f24%2Fimage.png")
]

for name, u in test_urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            print(f"Downloaded {name}: {len(data)} bytes, Content-Type: {resp.headers.get('Content-Type')}")
    except Exception as e:
        print(f"Error {name}: {e}")
