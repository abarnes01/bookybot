import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

df = pd.read_csv('kindle_notes.csv')

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        try:
            guild = discord.Object(id=1336386399854661642)
            synced = await self.tree.sync(guild=guild)
            print(f"Synced {len(synced)} commands to guild {guild.id}")
        except Exception as e:
            print(f"Error syncing commands: {e}")

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

GUILD_ID = discord.Object(id=1336386399854661642)

@client.tree.command(name="quote", description="Get a random quote from your kindle!", guild=GUILD_ID)
async def send_quote(interaction: discord.Interaction):

    row = df.sample().iloc[0]
    book, author, quote = row["book"], row["author"], row["quote"]
    if author == "Author Not Found":
        title = f"{book}"
    else:
        title = f"{book} by {author}"

    if quote[0].islower():
        quote = "..." + quote

    # Ellipsis when going over Discord embed limit
    if len(title) > 253:
        title = title[:250] + "..."

    embed = discord.Embed(title=title, description=f"**{quote}**", color=0x00FF00)
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
