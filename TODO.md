# 測試計畫

## test_ui.py（搜尋功能）

| 測試項目 | 狀態 |
|---|---|
| test_empty_string | ✅ |
| test_search_juice | ✅ |
| test_search_case_insensitive | ✅ |
| test_search_special_characters | ✅ |
| test_search_trim | ✅ |

## test_login.py（登入功能）

| 測試項目 | 狀態 |
|---|---|
| test_login_success | ✅ |
| test_login_wrong_password | ✅ |
| test_login_password_plaintext | ✅ |
| test_login_invalid_email | ✅ |
| test_login_sql_injection | ✅ |

## test_cart.py（購物車功能）

| 登入狀態 | 測試項目 | 狀態 |
|---|---|---|
| 未登入 | test_add_item_to_cart | ✅ |
| 未登入 | test_add_all_item_to_cart | ✅ |
| 未登入 | test_cart_item_count | ⬜ |
| 未登入 | test_remove_item_from_cart | ⬜ |
| 未登入 | test_update_item_quantity | ⬜ |
| 未登入 | test_checkout_without_login | ⬜ |
| 未登入 | test_cart_persistence_after_reload | ⬜ |
| 已登入 | test_cart_persistence_after_login | ⬜ |
| 已登入 | test_checkout_with_login | ⬜ |
