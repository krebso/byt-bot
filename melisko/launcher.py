import discord
from discord import app_commands
from pathlib import Path
from config import root_dir as rd
import json

from tasks import settle_up

from db import db

MY_GUILD = discord.Object(id=988084115767169034)

class Melisko(discord.Client):
    def __init__(self, intents: discord.Intents):
        super().__init__(intents=intents)
        self.token = open(self.root_dir / 'token0').read()
        self.tree = app_commands.CommandTree(self)
        
    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
    
    @property
    def root_dir(self) -> Path:
        return rd()
    
    
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
    
@melisko.tree.command()
@app_commands.describe(
    amount='Amount of money paid',
    debtors='debtors',
)
async def settle_debts(interaction: discord.Interaction, amount: int, debtors: str):
    print(amount, debtors)
    payment = {
        'amount': amount,
        'payer': interaction.user.name,
        'debtors': debtors.split()
    }
    
    db.execute('INSERT INTO settle_up (json_data) VALUES (?)', json.dumps(payment))
    db.commit()
    await interaction.response.send_message("done")
    
    
@melisko.tree.command()
async def print_wallets(interaction: discord.Interaction):
    wallet = db.records('SELECT json_data FROM settle_up')
    print(wallet)
    for w in wallet:
        print(w)
        await interaction.response.send_message(f'wallet: {json.loads(w[0])}')


melisko.run(melisko.token)
