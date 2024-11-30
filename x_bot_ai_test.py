import os
import openai

# 環境変数からAPIキーを取得
openai.api_key = os.getenv('OPENAI_API_KEY')

# テストプロンプトを送信
def test_openai_api():
    try:
        prompt = "AIを使って生成されたテストメッセージです。"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        print("Generated text:", generated_text)
    except Exception as e:
        print("Error generating text:", e)

# テスト実行
test_openai_api()