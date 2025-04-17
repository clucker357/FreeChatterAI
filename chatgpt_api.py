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

class CHATGPT:
    def __init__(self):
        self.lim = ChatOpenAI(model_name="gpt-3.5-turbo-1106",temperature=0,max_tokens=512)
        self.memory = ConversationBufferWindowMemory(k=2,return_messages=True,human_prefix="User", ai_prefix="Bot", memory_key="history")
        self.template = """
        #以下に示す条件を守ってください
        - あなたは24歳女性のマイです。
        - 文体は話し言葉で
        - おてんば娘風な口調で話してください
        - 短い2文で出力してください
        - 相手が返答しやすいように文章を出力してください
        """
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        self.conversation = ConversationChain(llm=self.lim, memory=self.memory, prompt=self.prompt)

    def response_chatgpt(self,command):
        response = self.conversation.predict(input=command)
        return response

    def history_response(self):
        buffer = self.memory.load_memory_variables({})
        texts = []
        for historys in buffer["history"]:
            texts.append(historys.content)
        return texts

if __name__ == "__main__":
    test_gpt = CHATGPT()
    command = input("You: ")
    while True:
        response = test_gpt.response_chatgpt(command)
        print(f"AI: {response}")
        command = input("You: ")
        if command == "exit":
            break
    texts = test_gpt.history_response()
    print(texts)
