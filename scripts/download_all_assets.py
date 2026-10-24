import os
import json
import urllib.request
import ssl
import hashlib
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://padlet.com/'
}

os.makedirs('assets/images', exist_ok=True)
os.makedirs('assets/files', exist_ok=True)

# 1. Download Wallpaper
bg_url = "https://v1.padlet.pics/1/image?t=c_lfill,dpr_1,f_auto,g_auto,h_1080,q_auto:best,w_1920&url=https%3A%2F%2Felvis.padletcdn.com%2F1%2Fatat%2Fe_in-u_1773398369%2FappbR1Qbe0DGnDKkS%2FtblhZFRy95OZHncLj%2FrecwPbXU3gjNY3Fit%2FfldJu5JvkUBo8MUFA"
bg_local = "assets/images/wallpaper.jpg"

try:
    print("Downloading wallpaper...")
    req = urllib.request.Request(bg_url, headers=headers)
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        with open(bg_local, 'wb') as f:
            f.write(resp.read())
    print("Downloaded wallpaper!")
except Exception as e:
    print("Wallpaper error:", e)

# 2. Download Specific Files
files_map = {
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/df8935d96eef982d28dcd34543dd5999/tw_spark_edu_lesson_pack_generator.zip": ("assets/files/tw_spark_edu_lesson_pack_generator.zip", "備課資料生成skill.zip"),
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/6966c939bfd3f65607d1d97a6690c9db/tw_spark_edu_lesson_pack_generator_genoffice_local.zip": ("assets/files/tw_spark_edu_lesson_pack_generator_genoffice_local.zip", "本地端技能-備課資料生成.zip"),
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/97bd14ec22dd012ab4adec5b91765598/10_____5_____07_____.pdf": ("assets/files/10_國小國語5上課本_第07課_學.pdf", "10_國小國語5上課本_第07課_(學).pdf"),
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/3a6698df981f2297db20edaf642de7c7/10_____5_____07_____.pdf": ("assets/files/10_國小國語5上課本_第07課_分科.pdf", "10_國小國語5上課本_第07課_(學)_分科.pdf"),
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/bec83d0808db2b5921330a89184b4560/Gem__.txt": ("assets/files/Gem範例-音樂生成助手.txt", "Gem範例-音樂生成助手.txt"),
    "https://padlet-artifacts.storage.googleapis.com/23652c81fe4cfd5f57640b795a7784aaa8809bfd/aff07bcfe899c550bf9d6d5436d825a9-h-0465417dd323b5ef1a31ece2fb7e1e6c.png": ("assets/files/範例教案_完整文件預覽.png", "範例教案_完整文件預覽.png")
}

url_to_local = {}

for u, (local_path, display_name) in files_map.items():
    print(f"Downloading file: {display_name}...")
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
            data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            print(f"  -> Saved {local_path} ({len(data)} bytes)")
            url_to_local[u] = local_path
    except Exception as e:
        print(f"  -> Error downloading {display_name}: {e}")

# 3. Download All Card Images
with open('data/all_image_urls.txt', 'r', encoding='utf-8') as f:
    img_urls = [line.strip() for line in f if line.strip()]

print(f"\nDownloading {len(img_urls)} card images...")

for idx, u in enumerate(img_urls):
    if u in url_to_local:
        continue
    
    # Generate clean unique filename
    h = hashlib.md5(u.encode('utf-8')).hexdigest()[:12]
    ext = '.webp'
    if '.png' in u.lower():
        ext = '.png'
    elif '.jpg' in u.lower() or '.jpeg' in u.lower():
        ext = '.jpg'
    elif '.svg' in u.lower():
        ext = '.svg'
        
    local_path = f"assets/images/img_{idx+1}_{h}{ext}"
    try:
        req = urllib.request.Request(u, headers=headers)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            data = resp.read()
            with open(local_path, 'wb') as f:
                f.write(data)
            url_to_local[u] = local_path
            print(f"[{idx+1}/{len(img_urls)}] Saved {local_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"[{idx+1}/{len(img_urls)}] Failed: {u[:60]}... ({e})")

print(f"\nTotal assets mapped to local: {len(url_to_local)}")
with open('data/url_to_local.json', 'w', encoding='utf-8') as f:
    json.dump(url_to_local, f, ensure_ascii=False, indent=2)

print("Saved data/url_to_local.json!")
