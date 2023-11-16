import os

from revChatGPT.V3 import Chatbot

# 没有设置OpenAI APIKey 时使用geekerwan自建端口
# os.environ['API_URL'] = "https://api.geekerwan.net/chatgpt2"
# mach_id = machine_id.get_machine_unique_identifier()
# api_key = mach_id

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
chatbot = Chatbot(api_key=OPENAI_API_KEY, proxy="http://127.0.0.1:7890")
print("Chatbot Start: ")
prev_text = ""
complete_text = ""
for data in chatbot.ask(
        "你现在要回复我一段中文的文字，这段文字需要超过两句话。回复中必须用中文标点。",
):
    message = data
    print(message, end="", flush=True)
    if "。" in message or "！" in message or "？" in message:
        print('')
        print(complete_text)
        complete_text = ""
    else:
        complete_text += message
    prev_text = data
print()
