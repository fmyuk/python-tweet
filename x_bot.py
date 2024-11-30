import tweepy
import schedule
import time
import openai
from datetime import datetime

# Twitter APIの認証情報
api_key = os.getenv('TWITTER_API_KEY')
api_secret_key = os.getenv('TWITTER_API_SECRET_KEY')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# OpenAI APIの認証情報
openai.api_key = os.getenv('OPENAI_API_KEY')

# 認証
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# OpenAIを使用して自動投稿の内容を生成する関数
def generate_tweet_content():
    prompt = "転職やエンジニアとしてのキャリアアップに関するアドバイスを140文字以内で教えてください。"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    tweet_content = response['choices'][0]['message']['content'].strip()
    return tweet_content

# 自動投稿を行う関数
def post_tweet():
    tweet_content = generate_tweet_content()
    try:
        api.update_status(tweet_content)
        print("Tweet posted:", tweet_content)
    except tweepy.TweepError as e:
        print("Error posting tweet:", e)

# 自動フォローを行う関数
def auto_follow():
    try:
        for tweet in tweepy.Cursor(api.search, q='転職 OR エンジニア', lang='ja').items(10):
            user_id = tweet.user.id
            api.create_friendship(user_id)
            print(f"Followed {tweet.user.screen_name}")
    except tweepy.TweepError as e:
        print("Error following user:", e)

# 自動リプライを行う関数
def auto_reply():
    try:
        for tweet in tweepy.Cursor(api.mentions_timeline).items(10):
            if not tweet.favorited:
                tweet.favorite()
                reply_text = generate_reply_content(tweet)
                api.update_status(f"@{tweet.user.screen_name} {reply_text}", in_reply_to_status_id=tweet.id)
                print(f"Replied to {tweet.user.screen_name}")
    except tweepy.TweepError as e:
        print("Error replying to tweet:", e)

# リプライ内容を生成する関数
def generate_reply_content(tweet):
    prompt = f"次のツイートに対するリプライを140文字以内で考えてください: {tweet.text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    reply_content = response['choices'][0]['message']['content'].strip()
    return reply_content

# スケジュール設定
schedule.every().day.at("09:00").do(post_tweet)
schedule.every().day.at("10:00").do(auto_follow)
schedule.every().hour.do(auto_reply)

# メインループ
while True:
    schedule.run_pending()
    time.sleep(1)