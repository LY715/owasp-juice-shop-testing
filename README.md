# Juice Shop UI 自動化測試

## 簡介
使用 Playwright + pytest 對 OWASP Juice Shop 進行自動化測試

## 環境需求
- Docker
- Python 3.x
- pytest
- playwright
- pytest-html
- Git

## 啟動 Juice Shop（Docker）
```
docker run -d -p 3000:3000 bkimminich/juice-shop
```
啟動後可在瀏覽器打開 http://localhost:3000 確認網站正常運作

## 安裝
```
pip install pytest playwright pytest-html
playwright install
```

## 執行測試
```
pytest --html=report.html --self-contained-html -v --log-cli-level=INFO --log-level=INFO
```

## 測試項目
- test_ui.py：搜尋功能測試（搜尋 juice、搜尋空字串）
- test_login.py：登入功能測試

## 查看報告

打開瀏覽器到 https://ly715.github.io/owasp-juice-shop-testing/report.html

## 測試時發現（Findings During Testing）

| 項目 | 說明 | 重現步驟 | 預期結果 | 實際結果 | 嚴重程度 |
|---|---|---|---|---|---|
| 密碼明文傳輸 | 登入時密碼以明文方式傳送，未進行前端加密處理 | 1. 打開 F12 → Network tab 2. 輸入帳密點擊 Log in 3. 查看 Request Payload | 密碼應經過加密後再傳輸 | 密碼以plain text直接傳送 | 高 |
| 前端未驗證 Email 格式 | 輸入不合規的Email格式, 如 admin#juice-sh.op 可以直接送出log in請求並未被擋下 | 1. 在Email欄位輸入 admin#juice-sh.op 2. 輸入任意密碼 3. 點擊Log in | 網頁上應顯示此為不合法的Email格式，因此無法點擊 Log in按鈕 | 無任何警語出現，可以點擊Log in按鈕 | 低 |