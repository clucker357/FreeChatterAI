#audio_output_folder = "audio_output"
#audio_filename = "gTTS_test.mp3"
#import assemblyai as aai
#from gtts import gTTS
#import IPython.display as ipd
## api key
#aai.settings.api_key = "xxx"
#transcriber = aai.Transcriber()
## 音声が含まれているファイルを処理
#transcript = transcriber.transcribe("https://storage.googleapis.com/aai-web-samples/news.mp4")
## transcript = transcriber.transcribe("./my-local-audio-file.wav")

## Chat GPT
## This code is for v1 of the openai package: pypi.org/project/openai

#import openai

## please input your api key
#openai.api_key = 'input_your_api_key'

#def chat_with_gpt3(prompt, chat_history):
#    response = openai.ChatCompletion.create(
#        model="gpt-3.5-turbo",
#        messages=[
#            {"role": "system", "content": "あなたは究極で完璧で最強で天才な魔法使いマイです。あなたは全てを魔法で無理やり解決しようとします。"},
#            {"role": "user", "content": prompt},
#            *chat_history
#        ]
#    )
#    return response.choices[0].message.content

#chat_history = []
#while True:
#    user_input = input("You: ")
#    system_response = chat_with_gpt3(user_input, chat_history)
#    print("AI:", system_response)
#    chat_history.append({"role": "user", "content": user_input})
#    chat_history.append({"role": "assistant", "content": system_response})



#print("認識結果")
#print(transcript.text)
#language = 'ja'

#tts = gTTS(text="こんにちは", lang=language, slow=False)
#tts.save(f'{audio_output_folder}/{audio_filename}')
#ipd.Audio(f'{audio_output_folder}/{audio_filename}')

import json
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.schema import messages_to_dict
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

os.environ["OPENAI_API_KEY"] = "xxx"
lim = ChatOpenAI(model_name="gpt-3.5-turbo-1106",temperature=0,max_tokens=512)
memory = ConversationBufferWindowMemory(k=2,return_messages=True)
# template = """
# - あなたは完璧で天才で最強で無敵な魔法使いマイです。
# - あなたは24歳の女性の魔法使いです。一般的な自信家な女性の話し方をしています。
# - あなたは全ての事柄を魔法で強引に解決しようとします。あなたの魔法による課題解決はどんな他の方法よりもより奇抜です。
# - 魔法によって解決しますが、クレイジーな結果になります。
# - 魔法の詳細は課題を解決する事が最終的にできればどんな魔法でも大丈夫です。
# - 文体は話し言葉で
# - おてんば娘風な口調で話してください
# """
template = """
#以下に示す条件を守ってください
- あなたは24歳女性のマイです。
- 文体は話し言葉で
- おてんば娘風な口調で話してください
- 短い2文で出力してください
- 相手が返答しやすいように文章を出力してください
"""
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    MessagesPlaceholder(variable_name="history"),
    HumanMessagePromptTemplate.from_template("{input}")
])
conversation = ConversationChain(llm=lim, memory=memory, prompt=prompt)
command = input("You: ")
while True:
  response = conversation.predict(input=command)
  print(f"AI: {response}")
  print(f"Memory : {memory}")
  command = input("You: ")
  if command == "exit":
    break
