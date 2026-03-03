import requests
import base64
import os
import json

# WordPress設定
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

file_path = 'articles.json'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    # ★ 1回の実行で「6件分」を処理する設定
    if len(articles) >= 6:
        # 上から6件を取得（日・英・中・韓・西・仏のセットを想定）
        batch_to_post = articles[:6]
        
        for post in batch_to_post:
            post_to_wp(post['title'], post['content'])
        
        # 投稿した6件をリストから一気に消して保存
        remaining = articles[6:]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(remaining, f, ensure_ascii=False, indent=4)
        print(f"本日分の6ヶ国語同時投稿が完了しました。残りストック: {len(remaining)}件")
    else:
        print(f"ストックが不足しています（現在{len(articles)}件）。最低6件必要です。")
else:
    print("articles.jsonが見つかりません。")
