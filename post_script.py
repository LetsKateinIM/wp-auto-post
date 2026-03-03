import requests
import base64
import os
import json

# 設定
WP_URL = "https://dmp.intimatemerger.com/shopify/wp-json/wp/v2/posts"
USER = os.environ.get('WP_USER')
PASSWORD = os.environ.get('WP_PASSWORD')

def post_to_wp(title, content):
    auth_str = f"{USER}:{PASSWORD}"
    token = base64.b64encode(auth_str.encode()).decode()
    headers = {'Authorization': f'Basic {token}'}
    payload = {'title': title, 'content': content, 'status': 'publish'}
    res = requests.post(WP_URL, headers=headers, json=payload)
    print(f"投稿結果: {title} ({res.status_code})")

# 1. 記事データを読み込む
file_path = 'articles.json'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    if articles:
        # 2. 一番上の記事を取得して投稿
        today_post = articles[0]
        post_to_wp(today_post['title'], today_post['content'])
        
        # 3. 投稿した記事をリストから消して保存（使い回さないため）
        remaining_articles = articles[1:]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(remaining_articles, f, ensure_ascii=False, indent=4)
        print("ストックを更新しました。")
    else:
        print("記事ストックが空です。")
else:
    print("articles.jsonが見つかりません。")
