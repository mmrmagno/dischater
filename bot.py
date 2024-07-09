import discord
from discord.ext import commands
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Get the API keys from environment variables
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALLOWED_CHANNEL_ID = int(os.getenv("ALLOWED_CHANNEL_ID"))

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Intents
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# File paths
MESSAGE_HISTORY_FILE = 'message_history.json'
PERSONALITY_FILE = 'personality.json'

# Load message history from file
def load_message_history():
    if os.path.exists(MESSAGE_HISTORY_FILE):
        with open(MESSAGE_HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

# Save message history to file
def save_message_history():
    with open(MESSAGE_HISTORY_FILE, 'w') as file:
        json.dump(message_history, file)

# Load personality from file
def load_personality():
    if os.path.exists(PERSONALITY_FILE):
        with open(PERSONALITY_FILE, 'r') as file:
            return json.load(file)
    return {"system_message": "You are a helpful assistant."}

# Save personality to file
def save_personality(personality):
    with open(PERSONALITY_FILE, 'w') as file:
        json.dump(personality, file)

# Initialize message history and personality
message_history = load_message_history()
personality = load_personality()

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    # Record the message in history
    message_history.append((message.author.name, message.content))
    save_message_history()
    
    # Call OpenAI API to generate a response
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": personality["system_message"]},
            {"role": "user", "content": message.content}
        ]
    )
    
    await message.channel.send(response.choices[0].message.content)

@bot.tree.command(name="chathist", description="Check previous messages")
async def chathist(interaction: discord.Interaction):
    if interaction.channel.id != ALLOWED_CHANNEL_ID:
        await interaction.response.send_message("You are not allowed to use this command in this channel.", ephemeral=True)
        return
    
    if not message_history:
        await interaction.response.send_message("No messages in history.", ephemeral=True)
        return
    
    history_text = "\n".join([f"{author}: {content}" for author, content in message_history])
    await interaction.response.send_message(f"Message History:\n{history_text}")

@bot.tree.command(name="wipehistory", description="Wipe the message history")
async def wipehistory(interaction: discord.Interaction):
    global message_history
    message_history = []
    save_message_history()
    await interaction.response.send_message("Message history wiped.", ephemeral=True)

@bot.tree.command(name="editpersonality", description="Edit the bot's personality")
async def editpersonality(interaction: discord.Interaction, new_personality: str):
    global personality
    personality["system_message"] = new_personality
    save_personality(personality)
    await interaction.response.send_message("Personality updated.", ephemeral=True)

bot.run(DISCORD_BOT_TOKEN)
