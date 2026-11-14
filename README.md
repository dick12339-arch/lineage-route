# 天堂路線（天堂1 亞丁大陸路線指引）

- 完整網頁版：https://dick12339-arch.github.io/lineage-route/
- 安裝書籤：https://dick12339-arch.github.io/lineage-route/install.html
- 書籤主程式：`l1.js`（優先由 https://dick12339-arch.github.io/lineage-route/l1.js 載入，備援 jsDelivr）

怪物與掉落資料取自「樂園 怪物查詢」https://joelbutaladr.github.io/linwebtw/

地圖圖片由 https://www.lcinfo.io/maps 於執行時載入，本儲存庫不含任何地圖檔。

版本資訊：v2.14（2026-11-14）— 工具新增「活動提醒」：自訂世界活動（名稱、星期、多個開始時間、每 N 小時快速產生、持續時間、提前提醒、地點、備註），到點在遊戲畫面上方跳橫幅＋響鈴＋震動（視窗收起也會跳），可一鍵導航、開關、編輯，活動表可匯出／匯入分享給盟友
- v2.13（2026-11-14）— 新增「NPC」分頁：搜尋 624 個 NPC 位置（名稱／地區／用途：傳送師、倉庫、商人、守護者），可依地區篩選、「離我最近」排序（需先輸入 /loc），在地圖上標示或一鍵導航；物品頁的商店與製作 NPC 可直接點過去查位置。資料取自 L1J-TW 開源資料庫（src/npcgen.py 可重新產生）
- v2.12（2026-11-14）— 工具「畫質／省電」新增提高畫質渲染：高（解除引擎 2 倍上限，用螢幕原生解析度）／超高／極致（超取樣），依 GPU 上限自動封頂；另有色彩增強、平滑貼圖與一鍵「✨ 高畫質」
- v2.11（2026-11-13）— 工具新增「省電」：鎖幀數、降低遊戲畫質、黑屏掛機、關閉工具動畫


## 開發（給新對話接手用）
- 原始檔：`src/lineage-map-guide.html`（唯一要改的檔）
- 建置：把 src 內檔案放成 `lineage-map-guide.html` + `build/make.py`、`build/install_tpl.html`、`build/game-land.js`，在上層執行 `python3 build/make.py lineage-map-guide.html`，產出 `build/l1.js`、`天堂路線指引.html`（→ index.html）、`安裝天堂書籤.html`（→ install.html）
- 更新資料：`python3 build/regen.py <linwebtw db.json> lineage-map-guide.html`
- 更新 NPC：clone https://github.com/L1Rj/L1j-TW 後執行 `python3 src/npcgen.py <L1j-TW>/db/InnoDB_TW src/lineage-map-guide.html`
- 每次更新：改頁首版本、make.py 標題列版本、README 版本資訊，再推送
