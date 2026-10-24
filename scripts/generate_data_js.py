import json

with open('board_final_polished.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

js_content = f"// Padlet Board Data - 從AI問答走向教學工作流1024\nwindow.INITIAL_BOARD_DATA = {json.dumps(data, ensure_ascii=False, indent=2)};\n"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Generated data.js successfully!")
