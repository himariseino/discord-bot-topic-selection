import discord
import os
from dotenv import load_dotenv

# 入力を受け取る
class InputHandler:
    def validate_input(self, user_input):
        if not user_input:
            raise ValueError("Input is empty!")
        return user_input.strip()
    
# LLMによる処理
class LLMProcessor:
    def __init__(self, model):
        self.model = model
    
    def process(self, input_text):
        # ダミーのLLM処理
        print(f"Processing with LLM: {input_text}")
        return f"Processed output for: {input_text}"
    
# 出力クラス
class OutputHandler:
    def format_output(self, result):
        return f"LLM Response: {result}"
    
    def send_output(self, channel, content):
        try:
            # Discordのチャンネルに送信する処理
            print(f"Sending to Discord: {content}")
        except Exception as e:
            print("Failed to send output: {e}")

# クラスを統合する上位管理クラス
class LLMService:
    def __init__(self, llm_model):
        self.input_handler = InputHandler()
        self.llm_processor = LLMProcessor(llm_model)
        self.output_handler = OutputHandler()
    
    async def handle_request(self, user_input, channel):
        try:
            # 入力処理
            validated_input = self.input_handler.validate_input(user_input)
            
            # LLM処理
            result = self.llm_processor.process(validated_input)

            # 出力処理
            formatted_output = self.output_handler.format_output(result)
            self.output_handler.send_output(channel, formatted_output)
        except ValueError as e:
            await channel.send(f"Input Error: {str(e)}")
        except Exception as e:
            await channel.send(f"Processing Error: {str(e)}")