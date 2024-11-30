import discord # discord APIのライブラリ
import os # 環境変数の操作
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

class DiscordBot:
    def __init__(self):
        """
        今回作成するアプリケーションの動作を管理するクラス
        """
        # .envファイルをロード
        load_dotenv()

        # 接続に必要なオブジェクトを生成
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.message_content = True
        
        # discordインスタンスを生成
        self.client = discord.Client(intents=intents)
        # イベントハンドラ（on_readyやon_messageなど）を設定するメソッドを呼び出す
        self.setup_events()

    def setup_events(self):
        @self.client.event
        async def on_ready():
            print(f'ログインしました：{self.client.user}')

        @self.client.event
        async def on_message(message):
            if message.author.bot:
                return
            
            print(f'Received message: {message.content}')

            if message.content.startswith('/inputmoji'):
                command_content = message.content.removeprefix('/inputmoji').strip()
                if command_content:
                    response = await self.process_with_llm(command_content)
                    await message.channel.send(response)
                else:
                    await message.channel.send('入力がありませんでした．')

    async def process_with_llm(self, command_content):
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
            # チェーンに入力を与え，LLMによる推論を実行
            llm_output = (prompt | llm).invoke({"command_content": command_content})

            print("LLM: SUCCESS")
            return llm_output
        except Exception as e:
            print("LLM: FAILED", e)
            return f'LLMによる処理でエラーが発生しました．：{e}'

    def run(self):
        TOKEN = os.getenv("TOKEN")
        if TOKEN:
            self.client.run(TOKEN)
        else:
            print("TOKENが設定されていません．")

# Botの起動とDiscordサーバーへの接続
if __name__ == "__main__":
    bot = DiscordBot()
    bot.run()