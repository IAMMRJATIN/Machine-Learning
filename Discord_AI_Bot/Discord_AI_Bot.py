import os
import discord
import openai

openai.api_key = os.getenv("Open_AI_API")
token = os.environ["SECRET_KEY"]

chat = ""


class MyClient(discord.Client):

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        global chat
        chat += f"{message.author}: {message.content}"
        # print(f'Message from {message.author}: {message.content}\n')
        if self.user != message.author:
            if self.user in message.mentions:
                channel = message.channel

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        prompt=f"{chat}\nJBS_AI_BOT: ",
                        temperature=1,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    messageToSend = response.choices[0].message.content
                    await channel.send(messageToSend)

                except Exception as e:
                    print(f"Error while connection OpenAI: {e}")
                    await channel.send(
                        "Sorry, I am not able to answer your question at this moment. Please try again later."
                    )


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
