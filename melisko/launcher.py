import os
import discord
from discord import app_commands
from pathlib import Path

MY_GUILD = discord.Object(id=988084115767169034)

class Melisko(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.token = open(self.root_dir / 'token0').read()
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
    
    @property
    def root_dir(self) -> Path:
        return Path(os.path.dirname(os.path.abspath(__file__)))
    
    
    async def on_ready(self):
        print('Logged on as', self.user)


intents = discord.Intents.default()
melisko = Melisko(intents=intents)

@melisko.event
async def on_ready():
    print(f'Logged in as {melisko.user} (ID: {melisko.user.id})')
    print('------')
    
    
@melisko.tree.command()
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"čau {interaction.user.name}, hehe kokod")


melisko.run(melisko.token)
