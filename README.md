# 從AI問答走向教學工作流1024 - 協作看板網頁版

> 原始來源：[Padlet 看板](https://padlet.com/inforissuescounseling/ai-1024-s024rz6mqadq3x83gbcw)  
> 作者：臺中市資訊教育議題分團輔導員 (moodlela)  
> 分類規則：**黃標是資料 (21)、紅標有範例 (13)、藍標歸工具 (13)、綠標要實作 (2)**  
> 🌐 **線上體驗網址 (GitHub Pages)**：[https://yaoshuchin.github.io/padlet-ai-1024/](https://yaoshuchin.github.io/padlet-ai-1024/)

---

## 🌟 內容與資源完全本機複製 (100% Offline Ready)
本專案已將原始 Padlet 的所有文字、**所有圖片預覽** 以及 **所有下載附件** 完全下載複製至本機，不依賴 Padlet CDN 或暫時性的 Token，離線也能完整使用！

### 📁 本機資源結構
* **`assets/images/`** (共 46 個圖片檔案)：
  * 看板高解析度黑板/軟木壁紙 (`wallpaper.jpg`)。
  * 每張便利貼的示意圖、截圖與各網站預覽縮圖。
* **`assets/files/`** (下載附件庫)：
  * `tw_spark_edu_lesson_pack_generator.zip` (備課資料生成 skill 壓縮包)
  * `tw_spark_edu_lesson_pack_generator_genoffice_local.zip` (本地端技能生成壓縮包)
  * `10_國小國語5上課本_第07課_學.pdf` (國小國語課本教材 PDF)
  * `10_國小國語5上課本_第07課_分科.pdf` (分科備課教材 PDF)
  * `Gem範例-音樂生成助手.txt` (自訂 Gem 音樂生成助手提示詞文字檔)
  * `範例教案_完整文件預覽.png` (範例教案 Word 完整文件高清版)

---

## 📋 15 個分欄主題
1. **說在前面** (自我介紹 Canva 簡報)
2. **今日講義** (AI 備課自動化工作流 Google 協作平台)
3. **相關平台** (Gemini、Workspace Studio、動態提示詞庫)
4. **個人化智慧服務** (連結的應用程式)
5. **問問Gemini** (問問Gemini、新聞範例、Skills指令集、測試連結應用程式功能、網頁內容比價等)
6. **實用Gem** (Gem特性/工具、如何撰寫自製Gem提示詞、紅焰系列 Gem 機器人、創用CC授權標註)
7. **Gem轉換為技能** (AI Skill 智慧開發工作台、Skills生成實作)
8. **Gemini-技能組合拳** (教案->規準->教學網、範例教案、真假訊息大偵探)
9. **延伸使用-(任務)** (Gemini效果、備課資料生成 skill .zip、國小國語課本 PDF、排程等)
10. **評分自動工作流** (Workspace Studio、測驗表單自動回饋、複製表單)
11. **額外補充** (預備分欄)
12. **Opencode本地端** (Opencode 下載、本地端技能生成包、課本教材)
13. **Gemini連動NB** (直接利用Gemini提問生成媒材、Gemini連動NBLM、NotebookLM 案例、範例指令)
14. **擴充程式** (OneTab、Typeless)
15. **作文批改** (PDF 上傳處理、翰林國中作文批改、康軒國語文寫作)

---

## 🚀 快速開啟方式
* **方式 1（直接點開）**：直接雙擊 [**`start.bat`**](./start.bat) 或直接用瀏覽器開啟 [**`index.html`**](./index.html)。
* **方式 2（本機靜態伺服器）**：
  ```bash
  npx serve .
  # 或
  python -m http.server 3000
  ```
  在瀏覽器開啟 `http://localhost:3000` 即可體驗！

---

## 💡 特色互動功能
* **三重視圖即時切換**：
  * 📌 **看板視圖 (Board / Shelf)**：15 欄水平滑動，支援滑鼠滾輪水平移動。
  * 🔲 **瀑布網格視圖 (Grid / Masonry)**：跨欄瀑布流排版，一覽所有卡片。
  * 📋 **清單視圖 (List View)**：緊湊清單，便於快速搜尋與批次查閱。
* **即時搜尋與標籤快速過濾**：
  * 輸入關鍵字即時搜尋標題、內文、提示詞與連結。
  * 標籤分類：全部 (49) / 🟡 資料 (21) / 🔴 範例 (13) / 🔵 工具 (13) / 🟢 實作 (2)。
* **便利貼深度互動**：
  * **本機檔案下載專區**：卡片上與彈窗中清楚標示本機檔案名稱與大小，點擊即可直接下載。
  * **圖片放大燈箱 (Lightbox)**：點擊圖片立即展開全螢幕檢視。
  * **一鍵複製**：卡片上或彈窗中直接一鍵複製提示詞到剪貼簿。
  * **愛心點讚**：支援卡片愛心點讚，並透過 LocalStorage 保存記錄。
  * **新增便利貼**：使用者可在任一分欄中點擊 `+` 新增自訂便利貼筆記。
