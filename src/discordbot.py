import discord
import os
from dotenv import load_dotenv
import langchain

# .envファイルをロード
load_dotenv()

# 接続に必要なオブジェクトを生成（有効なインデントのみ許可）
intents = discord.Intents.default()
intents.members = True  # メンバー関連のイベントを受け取る場合
intents.presences = True  # プレゼンス関連のイベントを受け取る場合
intents.message_content = True
client = discord.Client(intents=intents)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    print(f'Received message: {message.content}')
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    # 「/neko」と発言したら「にゃーん」が返る処理
    if message.content == '/neko':
        await message.channel.send('にゃーん')

# Botの起動とDiscordサーバーへの接続
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)

# # クラスを作成
# class MyClient(discord.Client):
#     async def on_ready