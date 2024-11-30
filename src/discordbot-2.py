import discord
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

# .envファイルをロード
load_dotenv()

# 接続に必要なオブジェクトを生成（有効なインデントのみ許可）
intents = discord.Intents.default()
intents.members = True  # メンバー関連のイベントを受け取る場合
intents.presences = True  # プレゼンス関連のイベントを受け取る場合
intents.message_content = True
client = discord.Client(intents=intents)

# 起動時の処理
@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')

# メッセージ受信時の処理
@client.event
# メッセージを受信し，次の処理へ渡す
async def on_message(message):
    if message.author.bot:
        return
    
    print(f'Received message: {message.content}')

    # "/inputmoji"コマンドの処理
    try:
        if message.content.startswith('/inputmoji'):
            command_content = message.content.removeprefix('/inputmoji') # discordで入力されたテキストを取得
            if command_content:
                response = await process_with_llm(command_content)
                await message.channel.send(response)
            else:
                await message.channel.send('入力がありませんでした．')
    except Exception as e:
        await message.channel.send(f'送信，またはLLMでエラーが発生しました．：{e}')

# LLMによる処理
async def process_with_llm(command_content):
    try:
        llm = OpenAI(temperature=0.7, max_tokens=100)
        prompt = PromptTemplate(
            input_variables=["command_content"],
            template="""
            You are given the following script:
            - script: {command_content}
            
            Understand this script and create more than 5 next class discussion's theme.
            """
        )
        # プロンプトとLLMをチェーンとして結合し，出力を文字列としてパース
        chain = prompt | llm

        # チェーンに入力を与え，LLMによる推論を実行
        llm_output = chain.invoke(
            {"command_content": command_content}
        )

        print("LLM: SUCCESS")
        return llm_output
    except Exception as e:
        print("LLM: FAILED", e)
        return f'LLMによる処理でエラーが発生しました．：{e}'
    
# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
    TOKEN = os.getenv("TOKEN")
    if TOKEN:
        client.run(TOKEN)
    else:
        print("TOKENが設定されていません．")