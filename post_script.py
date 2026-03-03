import requests
import base64
import os

# GitHub Secretsから情報を取得
WP_URL = "https://dmp.intimatemerger.com/shopify/wp-json/wp/v2/posts"
USER = os.environ.get('WP_USER')
PASSWORD = os.environ.get('WP_PASSWORD')

def post_to_wp(title, content):
    auth_str = f"{USER}:{PASSWORD}"
    token = base64.b64encode(auth_str.encode()).decode()
    headers = {'Authorization': f'Basic {token}'}
    payload = {'title': title, 'content': content, 'status': 'publish'}
    res = requests.post(WP_URL, headers=headers, json=payload)
    print(f"{title}: {res.status_code}")

# 今日の投稿内容（日本語3本 + 英語3本）
articles = [
    ("ShopifyとDMPの連携メリット", "DMPを導入することで、Shopify単体では見えない顧客行動が可視化されます。"),
    ("Benefits of Shopify & DMP Integration", "Integrating a DMP visualizes customer behavior not seen by Shopify alone."),
    ("2026年のECマーケティング動向", "AIによるパーソナライズの自動化が、ECサイトの標準になります。"),
    ("EC Marketing Trends 2026", "Automated AI personalization will become the standard for EC sites."),
    ("ファーストパーティデータの重要性", "サードパーティCookie廃止後、自社データの蓄積が最大の武器になります。"),
    ("Value of First-Party Data", "After the end of 3rd-party cookies, own data is the greatest weapon.")
]

for title, content in articles:
    post_to_wp(title, content)
