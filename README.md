# 天堂路線（天堂1 亞丁大陸路線指引）

- 完整網頁版：https://dick12339-arch.github.io/lineage-route/
- 安裝書籤：https://dick12339-arch.github.io/lineage-route/install.html
- 書籤主程式：`l1.js`（優先由 https://dick12339-arch.github.io/lineage-route/l1.js 載入，備援 jsDelivr）

怪物與掉落資料取自「樂園 怪物查詢」https://joelbutaladr.github.io/linwebtw/

地圖圖片由 https://www.lcinfo.io/maps 於執行時載入，本儲存庫不含任何地圖檔。

版本資訊：v2.11（2026-11-13）— 工具新增「省電」：鎖幀數（30/20/15）、降低遊戲畫質、黑屏掛機、關閉工具動畫，設定會記住並自動套用


## 開發（給新對話接手用）
- 原始檔：`src/lineage-map-guide.html`（唯一要改的檔）
- 建置：把 src 內檔案放成 `lineage-map-guide.html` + `build/make.py`、`build/install_tpl.html`、`build/game-land.js`，在上層執行 `python3 build/make.py lineage-map-guide.html`，產出 `build/l1.js`、`天堂路線指引.html`（→ index.html）、`安裝天堂書籤.html`（→ install.html）
- 更新資料：`python3 build/regen.py <linwebtw db.json> lineage-map-guide.html`
- 每次更新：改頁首版本、make.py 標題列版本、README 版本資訊，再推送
