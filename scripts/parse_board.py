import json
import re
from bs4 import BeautifulSoup

with open('padlet_rendered.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')

# Board metadata
title = "從AI問答走向教學工作流1024"
desc = "黃標是資料、紅標有範例、藍標歸工具、綠標要實作"
author = "臺中市資訊教育議題分團輔導員 (moodlela)"

# Let's find background wallpaper
bg_style = ""
body = soup.find('body')
if body and body.get('style'):
    bg_style = body.get('style')

# Load the RSS items as dictionary keyed by wish ID
with open('padlet_data.json', 'r', encoding='utf-8') as f:
    feed_data = json.load(f)

feed_dict = {}
for item in feed_data.get('items', []):
    guid = item.get('guid', '')
    m = re.search(r'/wish/(\d+)', guid)
    if m:
        feed_dict[m.group(1)] = item
    link = item.get('link', '')
    m2 = re.search(r'/wish/(\d+)', link)
    if m2:
        feed_dict[m2.group(1)] = item

print(f"Loaded {len(feed_dict)} items from feed.xml")

# Parse sections
# Look for sections by finding elements with data-testid="sectionTitleText"
sections = []
section_titles = soup.find_all(attrs={'data-testid': 'sectionTitleText'})

for st in section_titles:
    sec_title = st.get_text().strip()
    
    # Find section header wrapper to get background color
    sec_wrapper = st.find_parent(attrs={'style': re.compile(r'background-color')})
    sec_color = ""
    if sec_wrapper and 'background-color' in sec_wrapper.get('style', ''):
        m = re.search(r'background-color:\s*([^;]+)', sec_wrapper['style'])
        if m:
            sec_color = m.group(1).strip()
    
    # Find group posts container
    # Look for following group-posts div
    # Or find parent that contains group-posts
    parent_col = st.find_parent(attrs={'data-testid': lambda x: x and 'section' in str(x).lower()})
    if not parent_col:
        # traverse up
        p = st
        for _ in range(8):
            if p.parent:
                p = p.parent
                gp = p.find(attrs={'class': lambda c: c and 'group-posts' in c})
                if gp:
                    parent_col = p
                    break
    
    group_posts = parent_col.find(attrs={'class': lambda c: c and 'group-posts' in c}) if parent_col else None
    
    posts_data = []
    if group_posts:
        cards = group_posts.find_all(attrs={'class': lambda c: c and 'wish' in c and 'surface-post' in c})
        for card in cards:
            card_id = card.get('id', '').replace('wish-', '')
            data_id = card.get('data-id', card_id)
            color = card.get('data-color', '')
            
            # Card title
            subject_el = card.find(attrs={'id': re.compile(r'surface-post-subject')})
            card_title = subject_el.get_text().strip() if subject_el else ""
            
            # Card body
            body_el = card.find(attrs={'class': lambda c: c and 'body' in str(c)})
            card_body = body_el.decode_contents().strip() if body_el else ""
            
            # If empty, also check paragraphs inside card
            if not card_body:
                paras = card.find_all('p')
                if paras:
                    card_body = "".join(str(p) for p in paras)
            
            # Check attachment in card
            attachment = {}
            att_link = card.find('a', href=True)
            if att_link:
                attachment['href'] = att_link['href']
                attachment['text'] = att_link.get_text().strip()
            
            img = card.find('img')
            if img and img.get('src'):
                attachment['img_src'] = img['src']
                if img.get('alt'):
                    attachment['img_alt'] = img['alt']
            
            # Merge with feed_dict if available
            feed_info = feed_dict.get(str(data_id))
            if feed_info:
                if not card_title and feed_info.get('title'):
                    card_title = feed_info['title']
                if not card_body and feed_info.get('description'):
                    card_body = feed_info['description']
                if feed_info.get('enclosures'):
                    enc_url = feed_info['enclosures'][0].get('url', '')
                    if enc_url and not attachment.get('href') and not attachment.get('img_src'):
                        if enc_url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
                            attachment['img_src'] = enc_url
                        else:
                            attachment['href'] = enc_url
            
            posts_data.append({
                'id': data_id,
                'title': card_title,
                'body': card_body,
                'color': color,
                'attachment': attachment,
                'raw_text': card.get_text().strip()
            })
            
    sections.append({
        'title': sec_title,
        'color': sec_color,
        'posts': posts_data
    })

board_export = {
    'title': title,
    'description': desc,
    'author': author,
    'total_sections': len(sections),
    'sections': sections
}

with open('board_structured.json', 'w', encoding='utf-8') as f:
    json.dump(board_export, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(sections)} sections successfully!")
for s in sections:
    print(f"Section: {s['title']} ({len(s['posts'])} cards)")
