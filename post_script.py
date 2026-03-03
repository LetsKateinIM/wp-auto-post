import requests
import base64
import os
import json

WP_URL = "https://dmp.intimatemerger.com/shopify/wp-json/wp/v2/posts"
USER = os.environ.get('WP_USER')
PASSWORD = os.environ.get('WP_PASSWORD')

def post_to_wp(title, content):
    auth_str = f"{USER}:{PASSWORD}"
    token = base64.b64encode(auth_str.encode()).decode()
    headers = {'Authorization': f'Basic {token}'}
    payload = {'title': title, 'content': content, 'status': 'publish'}
    res = requests.post(WP_URL, headers=headers, json=payload)
    print(f"投稿完了: {title} ({res.status_code})")

# articles.json から今日の記事を取得する
if os.path.exists('articles.json'):
    with open('articles.json', 'r', encoding='utf-8') as f:
        all_articles = json.load(f)
    
    if all_articles:
        # 最初の1件（またはインデックス管理された記事）を投稿
        today_article = all_articles[0] 
        post_to_wp(today_article['title'], today_article['content'])
        
        # 投稿したものをリストから消して保存し直す（重複防止）
        remaining = all_articles[1:]
        with open('articles.json', 'w', encoding='utf-8') as f:
            json.dump(remaining, f, ensure_ascii=False, indent=4)
else:
    print("記事ストック(articles.json)が見つかりません。")
