from html.parser import HTMLParser
import re
import json

with open('padlet_rendered.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect how sections and cards are nested
# Look for column headers in the html
cols = [
    "說在前面", "自我介紹", "今日講義", "AI 備課自動化工作流", "相關平台",
    "Gemini", "Workspace Studio", "動態提示詞庫", "個人化智慧服務", "問問Gemini",
    "實用Gem", "Gem轉換為技能", "Gemini-技能組合拳", "延伸使用-(任務)", "評分自動工作流",
    "額外補充", "Opencode本地端", "Gemini連動NB", "擴充程式", "作文批改"
]

print("Length of HTML:", len(html))
for c in cols:
    pos = html.find(c)
    print(f"Col '{c}': pos {pos}")
