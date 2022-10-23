import os
import discord

client=discord.Client()
@client.event
async def on_ready():
    print("Logged in as {o.user}".format(Client))

@client.event
async def on_mess(message):
    if message.author==client.user:
        return;
    if message.client.startswith('$$'):
        await message.channel.send("Hello World")
    
client.run(os.getenv('token'))