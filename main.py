from azure.openai import Convo

chat = Convo()
print("Hello, what can I help you with today?")
user_message = input()

while user_message != "exit":
    print(chat.send_message(user_message))
    user_message = input()
