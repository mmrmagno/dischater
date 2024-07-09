import discord
from discord.ext import commands
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API keys from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Add this line to request message content intent

bot = commands.Bot(command_prefix='/', intents=intents)

# Store message history
message_history = []

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')
    await bot.tree.sync()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Record the message in history
    message_history.append((message.author.name, message.content))
    
    # Call OpenAI API to generate a response
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=f"The following is a conversation with a chatbot. The chatbot is friendly, creative, and always provides helpful responses.\n\nUser: {message.content}\nBot:",
        max_tokens=150
    )
    
    await message.channel.send(response.choices[0].text.strip())

@bot.command(name='history')
async def history(ctx):
    if not message_history:
        await ctx.send("No messages in history.")
        return
    
    history_text = "\n".join([f"{author}: {content}" for author, content in message_history])
    await ctx.send(f"Message History:\n{history_text}")

bot.run(DISCORD_BOT_TOKEN)
