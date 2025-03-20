from azure.openai import Convo
import asyncio
from websockets.asyncio.server import serve


async def handler(websocket):
    decider = Convo(max_tokens=10, prompt="decider_prompt.txt")
    chat = Convo(max_tokens=200, prompt="chat_prompt.txt")
    # recommender = Convo(max_tokens=300, prompt="recommend_prompt.txt")

    while True:
        user_message = await websocket.recv()
        print(user_message)

        # Returns 0 if the user is asking for a recommendation
        # Returns 1 if the user is asking a general question
        recommend_flag = decider.send_message(user_message)

        if recommend_flag == 0:
            # Classification model + Recommender goes here
            # predict = classification_model.predict(user_message)
            # Logic here to evaluate prediction and send message
            continue
        else:
            response = chat.send_message(user_message)
        await websocket.send(response)


async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
