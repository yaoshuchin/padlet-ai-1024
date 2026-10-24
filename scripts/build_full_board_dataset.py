import json
import re
from bs4 import BeautifulSoup

with open('padlet_ultrawide.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

with open('padlet_data.json', 'r', encoding='utf-8') as f:
    feed_data = json.load(f)

feed_dict = {}
for it in feed_data.get('items', []):
    guid = it.get('guid', '')
    m = re.search(r'/wish/(\d+)', guid)
    if m:
        feed_dict[m.group(1)] = it
    link = it.get('link', '')
    m2 = re.search(r'/wish/(\d+)', link)
    if m2:
        feed_dict[m2.group(1)] = it

# Board info
board_title = "從AI問答走向教學工作流1024"
board_desc = "黃標是資料、紅標有範例、藍標歸工具、綠標要實作"
author_name = "臺中市資訊教育議題分團輔導員"
bg_url = "https://v1.padlet.pics/1/image?t=c_lfill,dpr_1,f_auto,g_auto,h_1080,q_auto:best,w_1920&url=https%3A%2F%2Felvis.padletcdn.com%2F1%2Fatat%2Fe_in-u_1773398369%2FappbR1Qbe0DGnDKkS%2FtblhZFRy95OZHncLj%2FrecwPbXU3gjNY3Fit%2FfldJu5JvkUBo8MUFA"

# Find all section headers
sections = []
section_titles = soup.find_all(attrs={'data-testid': 'sectionTitleText'})

all_parsed_cards = []

for st in section_titles:
    st_title = st.get_text().strip()
    
    # Get color from parent
    # Look for style containing background-color
    sec_color = "#3b82f6"
    p = st
    for _ in range(5):
        if p.parent:
            p = p.parent
            if p.get('style') and 'background-color' in p['style']:
                m = re.search(r'background-color:\s*([^;]+)', p['style'])
                if m:
                    sec_color = m.group(1).strip()
                    break

    # Find the group-posts container
    gp = None
    curr = st
    for _ in range(10):
        if curr.parent:
            curr = curr.parent
            gp = curr.find(attrs={'class': lambda c: c and 'group-posts' in c})
            if gp:
                break
    
    cards_list = []
    if gp:
        card_nodes = gp.find_all(attrs={'class': lambda c: c and 'surface-post' in c and 'wish' in c})
        for cn in card_nodes:
            cid = cn.get('data-id') or cn.get('id', '').replace('wish-', '')
            data_color = cn.get('data-color', 'yellow')
            
            # Title
            sub = cn.find(attrs={'id': re.compile(r'surface-post-subject')})
            ctitle = sub.get_text().strip() if sub else ""
            
            # Body HTML
            body_div = cn.find(attrs={'class': lambda c: c and 'body' in str(c).lower() and 'wish' in str(c).lower()})
            if not body_div:
                body_div = cn.find(attrs={'class': lambda c: c and 'break-words' in str(c)})
            
            cbody = ""
            if body_div:
                cbody = body_div.decode_contents().strip()
            else:
                paras = cn.find_all('p')
                if paras:
                    cbody = "".join(str(p) for p in paras)

            # Attachments
            # Look for image
            img_tag = cn.find('img')
            img_src = img_tag.get('src') if img_tag else ""
            img_alt = img_tag.get('alt', '') if img_tag else ""
            
            # Look for link
            a_tag = cn.find('a', href=True)
            a_href = a_tag.get('href') if a_tag else ""
            a_text = a_tag.get_text().strip() if a_tag else ""

            # Feed fallback
            feed_item = feed_dict.get(str(cid))
            if feed_item:
                if not ctitle and feed_item.get('title'):
                    ctitle = feed_item['title']
                if not cbody and feed_item.get('description'):
                    cbody = feed_item['description']
                if feed_item.get('enclosures'):
                    enc = feed_item['enclosures'][0].get('url', '')
                    if enc:
                        if enc.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')) and not img_src:
                            img_src = enc
                        elif not a_href:
                            a_href = enc

            # Clean up body if it only contains the title
            if cbody and cbody == f"<p>{ctitle}</p>":
                cbody = ""

            # Determine tag info
            tag_type = "yellow"
            if "orange" in data_color or "red" in data_color:
                tag_type = "red"
            elif "blue" in data_color or "oceanic" in data_color:
                tag_type = "blue"
            elif "green" in data_color:
                tag_type = "green"
            elif "yellow" in data_color or "canary" in data_color:
                tag_type = "yellow"
            elif "purple" in data_color:
                tag_type = "purple"
            else:
                tag_type = data_color or "yellow"

            card_obj = {
                'id': cid,
                'title': ctitle,
                'body': cbody,
                'color': tag_type,
                'raw_color': data_color,
                'image': img_src,
                'image_alt': img_alt,
                'link': a_href,
                'link_text': a_text
            }
            cards_list.append(card_obj)
            all_parsed_cards.append(card_obj)

    sections.append({
        'title': st_title,
        'color': sec_color,
        'cards_count': len(cards_list),
        'cards': cards_list
    })

board_final = {
    'title': board_title,
    'description': board_desc,
    'author': author_name,
    'background': bg_url,
    'total_sections': len(sections),
    'total_cards': len(all_parsed_cards),
    'sections': sections
}

with open('padlet_full_data.json', 'w', encoding='utf-8') as f:
    json.dump(board_final, f, ensure_ascii=False, indent=2)

print(f"DONE! Exported {len(sections)} sections, {len(all_parsed_cards)} cards.")
for s in sections:
    print(f"  [{s['title']}]: {s['cards_count']} cards")
