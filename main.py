import discord
import os
import requests
import json
import time
from discord.ext import commands
from discord import app_commands

# Environment variable handling with error checking
token = os.environ.get('TOKEN')
aikey = os.environ.get('DeepseekR1')

if not token or not aikey:
    raise ValueError("Missing required environment variables: TOKEN and/or DeepseekR1")

def chat_response(prompt):
    # List of models to try in order
    models_to_try = [
        "deepseek/deepseek-r1-zero:free",
        "deepseek/deepseek-r1-distill-llama-70b:free",
        "deepseek/deepseek-r1-distill-qwen-32b:free",
        "google/gemini-2.0-pro-exp-02-05:free",
        "openai/gpt-3.5-turbo:free",
        "anthropic/claude-instant-v1:free",
        "meta-llama/llama-2-13b-chat:free",
        "google/palm-2-chat-bison:free"
    ]

    for model in models_to_try:
        try:
            print(f"Trying model: {model}")

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {aikey}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://discord-bot.example.com",
                    "X-Title": "Discord Bot"
                },
                data=json.dumps({
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant replying to a user on Discord."
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                })
            )

            # Print debugging info
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text[:200]}...")

            if response.status_code == 200:
                response_data = response.json()
                content = response_data.get('choices', [{}])[0].get('message', {}).get('content', '')

                if content and content.strip():
                    print(f"Success with model {model}")
                    return content
                else:
                    print(f"Empty response from {model}")
            else:
                print(f"Error status code from {model}: {response.status_code}")

            # Wait briefly before trying next model to avoid rate limits
            time.sleep(1)

        except Exception as e:
            print(f"Exception with {model}: {str(e)}")
            continue

    # If we get here, all models failed
    return "I'm having trouble connecting to AI services right now. Please try again later."

def get_quote():
    try:
        response = requests.get(url="https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        return quote
    except Exception as e:
        return f"Error fetching quote: {str(e)}"


def get_meme():
    try:
         response = requests.get("https://meme-api.com/gimme")
         meme_data = response.json()
         return meme_data['url']
    except:
         return "Couldn't fetch a meme 😢"

# Set up Discord client with necessary permissions
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)



class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Greets the user")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Hello, {interaction.user.mention}!")



class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('maxx hello'):
            await message.channel.send('Hello!')

        if message.content.startswith('maxx motivate'):
            quote = get_quote()
            await message.channel.send(quote)

        if message.content.startswith('maxx chat'):
            prompt = message.content[9:].strip()  # Extract text after "maxx chat"
            if prompt:
                thinking_msg = await message.channel.send("Thinking...")

                # Test the API with a simple prompt first
                if prompt.lower() == "test":
                    await thinking_msg.edit(content="Testing API connection...")
                    test_response = chat_response("Say 'API is working!' if you can see this message.")
                    await message.channel.send(f"API Test Result: {test_response}")
                else:
                    ai_reply = chat_response(prompt)
                    await thinking_msg.delete()
                    await message.channel.send(ai_reply)
            else:
                await message.channel.send("Please provide a question or prompt after 'maxx chat'")

        # Add a diagnostic command
        if message.content.startswith('maxx diagnose'):
            await message.channel.send("Running API diagnostics...")
            try:
                # Simple non-sensitive request to test API connectivity
                response = requests.get("https://openrouter.ai/api/v1/models", 
                                      headers={"Authorization": f"Bearer {aikey}"})

                if response.status_code == 200:
                    models_data = response.json()
                    free_models = [model['id'] for model in models_data['data'] 
                                  if ':free' in model['id']][:5]
                    await message.channel.send(f"API connection successful. Available free models: {', '.join(free_models)}")
                else:
                    await message.channel.send(f"API connection failed with status code {response.status_code}")
            except Exception as e:
                await message.channel.send(f"API diagnostic error: {str(e)}")
        if message.content.startswith('maxx ping'):
            latency = round(self.latency * 1000)  # Convert latency to milliseconds
            await message.channel.send(f"Pong!  🏓   Latency: {latency}ms")

        if message.content.startswith('maxx antispam'):
            if message.author.guild_permissions.manage_messages:
                try:
                    # Split the message content into parts
                    parts = message.content.split()

                    # Check if there are enough parts
                    if len(parts) < 2:
                        await message.channel.send("Please provide a valid number! Example: `maxx clear 5`")
                        return

                    # Try to get the number from the correct position
                    amount = int(parts[2] if len(parts) > 2 else parts[1])

                    # Make sure the amount is positive
                    if amount <= 0:
                        await message.channel.send("Please provide a positive number!")
                        return

                    # Perform the purge operation
                    deleted = await message.channel.purge(limit=amount + 1)
                    await message.channel.send(f"Deleted {len(deleted)-1} messages!", delete_after=5)

                except ValueError:
                    # Specific error for non-integer input
                    await message.channel.send("Please provide a valid number! Example: `maxx clear 5`")
                except Exception as e:
                    # Handle other errors like missing permissions
                    await message.channel.send(f"An error occurred: {str(e)}")
            else:
                await message.channel.send("You don't have permission to use this command.")

            
        if message.content.startswith('maxx meme'):
             meme_url = get_meme()
             await message.channel.send(meme_url)




client = MyClient(intents=intents)
client.run(token)