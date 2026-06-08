# Juice Shop UI & API 自動化測試

## 簡介
使用 Playwright + pytest 對 OWASP Juice Shop 進行自動化測試

## 環境需求
- Docker
- Python 3.x
- pytest
- playwright
- pytest-html

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
```
python -m http.server 8080
```
打開瀏覽器到 http://localhost:8080/report.html
