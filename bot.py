import discord
import requests
import os
from discord.ext import commands
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
HF_API_KEY = os.getenv("HF_API_KEY")

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

# Hugging Face model endpoint
HF_MODEL = "gpt2"

# Function to query Hugging Face
def query_huggingface(payload):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(
        f"https://api-inference.huggingface.co/models/{HF_MODEL}",
        headers=headers,
        json=payload
    )
    try:
        return response.json()  # Attempt to return the JSON response
    except ValueError:
        return {"error": "Invalid JSON response"}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!ask'):
        query = message.content[len('!ask '):]
        try:
            # Query the Hugging Face model
            response = query_huggingface({"inputs": query})
            print("Hugging Face Response:", response)  # Log the response

            if isinstance(response, list):
                reply = response[0].get('generated_text', 'No response generated.')
            elif isinstance(response, dict) and 'error' in response:
                reply = f"Error: {response['error']}"
            else:
                reply = "Unexpected response format."

            await message.channel.send(reply)

        except Exception as e:
            await message.channel.send("An error occurred.")
            print(f"Error: {e}")

# Run the bot
bot.run(DISCORD_TOKEN)
