import discord
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

        try:
            guild = discord.Object(id=1336386399854661642)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f"Hello there {message.author}!")


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1336386399854661642)

@client.tree.command(name="quote", description="Get a random quote from your kindle!", guild=GUILD_ID)
async def send_quote(interaction: discord.Interaction):
    embed = discord.Embed(title=f"📖 Book title by Author Name", description=f"**Really long quote here, thats interesting**", color=0x00FF00)
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)