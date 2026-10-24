import json
import re
from bs4 import BeautifulSoup

with open('padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

with open('padlet_data.json', 'r', encoding='utf-8') as f:
    feed_data = json.load(f)

feed_map = {}
for it in feed_data.get('items', []):
    guid = it.get('guid', '')
    cid = guid.split('/')[-1] if '/' in guid else ''
    feed_map[cid] = it

# Board info
board = {
    "title": "從AI問答走向教學工作流1024",
    "subtitle": "黃標是資料、紅標有範例、藍標歸工具、綠標要實作",
    "author": {
        "name": "臺中市資訊教育議題分團輔導員",
        "username": "moodlela",
        "avatar": "https://lh3.googleusercontent.com/a-/AOh14GjPK1fXgOnYOp82G4gm3oLfMu1HMtLHXrYw3CR8=s96-c"
    },
    "date": "2026-10-24",
    "background": "https://v1.padlet.pics/1/image?t=c_lfill,dpr_1,f_auto,g_auto,h_1080,q_auto:best,w_1920&url=https%3A%2F%2Felvis.padletcdn.com%2F1%2Fatat%2Fe_in-u_1773398369%2FappbR1Qbe0DGnDKkS%2FtblhZFRy95OZHncLj%2FrecwPbXU3gjNY3Fit%2FfldJu5JvkUBo8MUFA",
    "columns": []
}

# Color mapping helper
def map_color(c_name):
    c_name = (c_name or '').lower()
    if 'orange' in c_name:
        return {'code': 'yellow', 'label': '資料', 'badge': 'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-900/40 dark:text-amber-200'}
    elif 'red' in c_name:
        return {'code': 'red', 'label': '範例', 'badge': 'bg-rose-100 text-rose-800 border-rose-300 dark:bg-rose-900/40 dark:text-rose-200'}
    elif 'blue' in c_name or 'oceanic' in c_name:
        return {'code': 'blue', 'label': '工具', 'badge': 'bg-sky-100 text-sky-800 border-sky-300 dark:bg-sky-900/40 dark:text-sky-200'}
    elif 'green' in c_name:
        return {'code': 'green', 'label': '實作', 'badge': 'bg-emerald-100 text-emerald-800 border-emerald-300 dark:bg-emerald-900/40 dark:text-emerald-200'}
    return {'code': 'yellow', 'label': '資料', 'badge': 'bg-amber-100 text-amber-800 border-amber-300'}

# Detect attachment type
def get_attachment_type(url):
    if not url:
        return None
    url_low = url.lower()
    if url_low.endswith(('.zip', '.rar', '.7z')):
        return {'type': 'archive', 'label': '下載技能/壓縮包'}
    if url_low.endswith('.pdf'):
        return {'type': 'pdf', 'label': 'PDF 課本教材'}
    if url_low.endswith(('.docx', '.doc')):
        return {'type': 'doc', 'label': 'Word 教案文件'}
    if 'forms.gle' in url_low or 'docs.google.com/forms' in url_low:
        return {'type': 'form', 'label': 'Google 表單'}
    if 'gemini.google.com/gem' in url_low:
        return {'type': 'gem', 'label': '自訂 Gem'}
    if 'share.gemini.google' in url_low or 'gemini.google.com' in url_low:
        return {'type': 'gemini', 'label': 'Gemini 成果分享'}
    if 'notebook.google.com' in url_low:
        return {'type': 'notebook', 'label': 'NotebookLM 筆記本'}
    if 'canva.' in url_low:
        return {'type': 'canva', 'label': 'Canva 簡報講義'}
    if 'sites.google.com' in url_low:
        return {'type': 'site', 'label': 'Google 網站'}
    if 'chromewebstore.google.com' in url_low:
        return {'type': 'extension', 'label': 'Chrome 擴充套件'}
    if url_low.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        return {'type': 'image', 'label': '圖片預覽'}
    return {'type': 'link', 'label': '外部連結'}

# Extract section headers
section_titles = soup.find_all(attrs={'data-testid': 'sectionTitleText'})

col_idx = 1
for st in section_titles:
    sec_title = st.get_text().strip()
    
    # Header color
    sec_color = "rgb(73, 123, 199)"
    p = st
    for _ in range(5):
        if p.parent:
            p = p.parent
            if p.get('style') and 'background-color' in p['style']:
                m = re.search(r'background-color:\s*([^;]+)', p['style'])
                if m:
                    sec_color = m.group(1).strip()
                    break

    # Find group posts
    gp = None
    curr = st
    for _ in range(10):
        if curr.parent:
            curr = curr.parent
            gp = curr.find(attrs={'class': lambda c: c and 'group-posts' in c})
            if gp:
                break
    
    cards = []
    if gp:
        # Find all actual wish cards (ignore inner surface-post-body)
        card_nodes = gp.find_all(attrs={'class': lambda c: c and 'surface-post' in c and 'wish' in c})
        card_nodes = [c for c in card_nodes if not c.get('id', '').startswith('surface-post-body')]
        
        for cn in card_nodes:
            cid = cn.get('data-id') or cn.get('id', '').replace('wish-', '')
            data_color = cn.get('data-color', 'orange')
            color_info = map_color(data_color)
            
            # Title
            sub = cn.find(attrs={'id': re.compile(r'surface-post-subject')})
            ctitle = sub.get_text().strip() if sub else ""
            
            # Feed match
            feed_it = feed_map.get(str(cid), {})
            if not ctitle and feed_it.get('title'):
                ctitle = feed_it['title']
                
            # Body
            cbody = ""
            body_div = cn.find(attrs={'class': lambda c: c and 'break-words' in str(c)})
            if body_div:
                cbody = body_div.decode_contents().strip()
            elif feed_it.get('description'):
                cbody = feed_it['description']

            # Attachments
            img_tag = cn.find('img')
            img_src = img_tag.get('src') if img_tag else ""
            img_alt = img_tag.get('alt', '') if img_tag else ""
            
            a_tag = cn.find('a', href=True)
            a_href = a_tag.get('href') if a_tag else ""
            
            # Clean up padlet wish internal redirects if feed has real link
            feed_enc = feed_it.get('enclosures', [{}])[0].get('url', '') if feed_it.get('enclosures') else ''
            
            final_link = ""
            if feed_enc and not feed_enc.startswith('https://padlet.com/'):
                final_link = feed_enc
            elif a_href and not a_href.startswith('https://padlet.com/'):
                final_link = a_href
            elif feed_enc:
                final_link = feed_enc
            elif a_href:
                final_link = a_href

            # Image resolution
            final_img = ""
            if img_src:
                final_img = img_src
            elif feed_enc and feed_enc.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                final_img = feed_enc

            att_meta = get_attachment_type(final_link)

            # Special case for pure prompt / instruction card
            is_prompt = False
            if '提示詞' in ctitle or '提示詞' in cbody or '範例指令' in ctitle or '/tw-spark' in cbody:
                is_prompt = True

            cards.append({
                "id": str(cid),
                "title": ctitle,
                "body": cbody,
                "color": color_info['code'],
                "color_label": color_info['label'],
                "badge_class": color_info['badge'],
                "image": final_img,
                "image_alt": img_alt,
                "link": final_link,
                "attachment_type": att_meta['type'] if att_meta else None,
                "attachment_label": att_meta['label'] if att_meta else None,
                "is_prompt": is_prompt,
                "likes": 0
            })

    board["columns"].append({
        "id": f"col-{col_idx}",
        "title": sec_title,
        "color": sec_color,
        "cards_count": len(cards),
        "cards": cards
    })
    col_idx += 1

with open('board_clean.json', 'w', encoding='utf-8') as f:
    json.dump(board, f, ensure_ascii=False, indent=2)

print("Saved board_clean.json successfully!")
print(f"Columns: {len(board['columns'])}")
total_cards = sum(len(c['cards']) for c in board['columns'])
print(f"Total cards: {total_cards}")
