import json
import re

with open('board_clean.json', 'r', encoding='utf-8') as f:
    board = json.load(f)

for col in board['columns']:
    for card in col['cards']:
        title = card['title'].strip()
        body = card['body'].strip()

        # If body is just the title wrapped in p or bare
        clean_body_text = re.sub(r'<[^>]+>', '', body).strip()
        if clean_body_text == title:
            card['body'] = ""
        
        # Link label enhancement
        link = card.get('link', '')
        if link:
            if 'canva.' in link:
                card['link_domain'] = 'Canva'
            elif 'gemini.google.com/gem' in link:
                card['link_domain'] = 'Gemini Gem'
            elif 'share.gemini.google' in link or 'gemini.google.com' in link:
                card['link_domain'] = 'Google Gemini'
            elif 'notebook.google.com' in link:
                card['link_domain'] = 'NotebookLM'
            elif 'studio.workspace.google.com' in link:
                card['link_domain'] = 'Workspace Studio'
            elif 'docs.google.com/forms' in link:
                card['link_domain'] = 'Google Forms'
            elif 'sites.google.com' in link:
                card['link_domain'] = 'Google Sites'
            elif 'moodlela914.github.io' in link:
                card['link_domain'] = 'GitHub Pages'
            elif 'opencode.ai' in link:
                card['link_domain'] = 'OpenCode AI'
            elif 'chromewebstore' in link:
                card['link_domain'] = 'Chrome Web Store'
            elif 'cna.com.tw' in link:
                card['link_domain'] = '中央通訊社'
            elif 'hle.com.tw' in link:
                card['link_domain'] = '翰林國中作文'
            elif 'knsh.com.tw' in link:
                card['link_domain'] = '康軒國語文寫作'
            elif 'typeless.com' in link:
                card['link_domain'] = 'Typeless'
            elif 'vocus.cc' in link:
                card['link_domain'] = '方格子 Vocus'
            elif 'creativecommons.org' in link:
                card['link_domain'] = 'Creative Commons'
            elif link.endswith('.zip') or 'download=1' in link:
                card['link_domain'] = '檔案下載 (.ZIP)'
            elif link.endswith('.pdf'):
                card['link_domain'] = '教材文件 (.PDF)'
            elif link.endswith('.docx'):
                card['link_domain'] = '教案範本 (.DOCX)'
            else:
                card['link_domain'] = '相關連結'

with open('board_final_polished.json', 'w', encoding='utf-8') as f:
    json.dump(board, f, ensure_ascii=False, indent=2)

print("Saved board_final_polished.json successfully!")
