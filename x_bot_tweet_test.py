import os
import tweepy

# 環境変数からAPIキーを取得
api_key = os.getenv('TWITTER_API_KEY')
api_secret_key = os.getenv('TWITTER_API_SECRET_KEY')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# 認証
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# テストツイートを投稿
def test_twitter_api():
    try:
        tweet_content = "これはテストツイートです。 #テスト"
        api.update_status(tweet_content)
        print("Tweet posted successfully:", tweet_content)
    except Exception as e:
        print("Error posting tweet:", e)

# テスト実行
test_twitter_api()