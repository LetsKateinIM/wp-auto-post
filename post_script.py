import requests
import base64
import os
import json
import time
from deep_translator import GoogleTranslator

# WordPress設定
WP_URL = "https://dmp.intimatemerger.com/shopify/wp-json/wp/v2/posts"
USER = os.environ.get('WP_USER')
PASSWORD = os.environ.get('WP_PASSWORD')

# 投稿する言語リスト (ISOコード)
LANGUAGES = {
    'en': 'English',
    'zh-CN': 'Chinese (Simplified)',
    'ko': 'Korean',
    'es': 'Spanish',
    'fr': 'French'
}

def post_to_wp(title, content):
    auth_str = f"{USER}:{PASSWORD}"
    token = base64.b64encode(auth_str.encode()).decode()
    headers = {'Authorization': f'Basic {token}'}
    payload = {'title': title, 'content': content, 'status': 'publish'}
    try:
        res = requests.post(WP_URL, headers=headers, json=payload)
        print(f"投稿完了: {title} ({res.status_code})")
    except Exception as e:
        print(f"エラー: {e}")

def translate_text(text, target_lang):
    """Google翻訳(無料枠)を使用して翻訳"""
    try:
        return GoogleTranslator(source='auto', target=target_lang).translate(text)
    except Exception as e:
        print(f"翻訳エラー({target_lang}): {e}")
        return text

# 1. 記事データを読み込む
file_path = 'articles.json'
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        articles = json.load(f)
    
    if articles:
        # 2. 一番上の記事（日本語）を取得
        today_post = articles[0]
        original_title = today_post['title']
        original_content = today_post['content']

        # まず日本語を投稿
        post_to_wp(original_title, original_content)

        # 3. 他の5言語に翻訳して投稿
        for lang_code, lang_name in LANGUAGES.items():
            print(f"{lang_name}に翻訳中...")
            translated_title = translate_text(original_title, lang_code)
            translated_content = translate_text(original_content, lang_code)
            
            post_to_wp(translated_title, translated_content)
            time.sleep(1) # サーバー負荷軽減

        # 4. 完了後、ストックから削除して保存
        remaining_articles = articles[1:]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(remaining_articles, f, ensure_ascii=False, indent=4)
        print("本日分の多言語投稿がすべて完了しました。")
    else:
        print("記事ストックが空です。")
else:
    print("articles.jsonが見つかりません。")
