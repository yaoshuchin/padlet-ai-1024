import json
import os

with open('data/url_to_local.json', 'r', encoding='utf-8') as f:
    url_to_local = json.load(f)

with open('data/board.json', 'r', encoding='utf-8') as f:
    board = json.load(f)

# Update background
board['background'] = 'assets/images/wallpaper.jpg'

# Specific file mappings for attachments
custom_file_links = {
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/df8935d96eef982d28dcd34543dd5999/tw_spark_edu_lesson_pack_generator.zip": {
        "local_file": "assets/files/tw_spark_edu_lesson_pack_generator.zip",
        "file_name": "tw_spark_edu_lesson_pack_generator.zip",
        "file_size": "3.8 KB",
        "file_type": "ZIP 技能壓縮包"
    },
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/6966c939bfd3f65607d1d97a6690c9db/tw_spark_edu_lesson_pack_generator_genoffice_local.zip": {
        "local_file": "assets/files/tw_spark_edu_lesson_pack_generator_genoffice_local.zip",
        "file_name": "tw_spark_edu_lesson_pack_generator_genoffice_local.zip",
        "file_size": "3.1 KB",
        "file_type": "ZIP 本地技能包"
    },
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/97bd14ec22dd012ab4adec5b91765598/10_____5_____07_____.pdf": {
        "local_file": "assets/files/10_國小國語5上課本_第07課_學.pdf",
        "file_name": "10_國小國語5上課本_第07課_(學).pdf",
        "file_size": "3.4 MB",
        "file_type": "PDF 課本教材"
    },
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/3a6698df981f2297db20edaf642de7c7/10_____5_____07_____.pdf": {
        "local_file": "assets/files/10_國小國語5上課本_第07課_分科.pdf",
        "file_name": "10_國小國語5上課本_第07課_(學)_分科.pdf",
        "file_size": "3.4 MB",
        "file_type": "PDF 課本教材"
    },
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/bec83d0808db2b5921330a89184b4560/Gem__.txt": {
        "local_file": "assets/files/Gem範例-音樂生成助手.txt",
        "file_name": "Gem範例-音樂生成助手.txt",
        "file_size": "3.5 KB",
        "file_type": "TXT 提示詞範例"
    },
    "https://padlet-uploads-usc1.storage.googleapis.com/1736270122/094571458e1d9ef6a1851ec6eb3fcea2/____.docx": {
        "local_file": "assets/files/範例教案_完整文件預覽.png",
        "file_name": "範例教案_完整文件預覽.png",
        "file_size": "300 KB",
        "file_type": "教案文件高清預覽"
    }
}

updated_cards = 0
for col in board['columns']:
    for card in col['cards']:
        remote_img = card.get('image', '')
        if remote_img:
            # Check direct match
            if remote_img in url_to_local:
                card['local_image'] = url_to_local[remote_img]
                card['original_image'] = remote_img
                card['image'] = url_to_local[remote_img]
                updated_cards += 1
            else:
                # Check url-encoded match
                clean_u = remote_img.replace('&amp;', '&')
                if clean_u in url_to_local:
                    card['local_image'] = url_to_local[clean_u]
                    card['original_image'] = clean_u
                    card['image'] = url_to_local[clean_u]
                    updated_cards += 1

        link = card.get('link', '')
        if link:
            card['original_link'] = link
            for remote_f, f_meta in custom_file_links.items():
                if remote_f in link or (card.get('id') == '4113216291' and '094571458' in remote_f):
                    card['local_file'] = f_meta['local_file']
                    card['file_name'] = f_meta['file_name']
                    card['file_size'] = f_meta['file_size']
                    card['file_type'] = f_meta['file_type']
                    # For downloads, prefer local file link!
                    card['link'] = f_meta['local_file']
                    card['link_domain'] = f"本機檔案 ({f_meta['file_type']})"
                    break

print(f"Updated {updated_cards} cards with local images and files!")

with open('data/board.json', 'w', encoding='utf-8') as f:
    json.dump(board, f, ensure_ascii=False, indent=2)

with open('board_final_polished.json', 'w', encoding='utf-8') as f:
    json.dump(board, f, ensure_ascii=False, indent=2)

js_content = f"// Padlet Board Data with Local Assets - 從AI問答走向教學工作流1024\nwindow.INITIAL_BOARD_DATA = {json.dumps(board, ensure_ascii=False, indent=2)};\n"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Saved data.js with local paths!")
