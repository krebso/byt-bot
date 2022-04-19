from asyncio import sleep
from glob import glob
from discord.ext.commands import Bot, CommandNotFound
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from ..db import db

TOKEN_PATH = "./dc_bot_i_pass_butter/lib/bot/token.0"
DC_BOT_PREFIX = '$'
OWNER_ID = '291691766250471435'
SERVER_ID = 826572526573322270
INPUT_CHANNEL_ID = 965007985451630633
OUTPUT_CHANNEL_ID = 965007985451630633
USERS_IDS = [291691766250471435]
COGS = [path.split('/')[-1][:-3] for path in glob('./dc_bot_i_pass_butter/lib/cogs/*.py')]


class Ready(object):
    def __init__(self) -> None:
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f'\t{cog} cog ready.')

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class I_pass_butter(Bot):

    def __init__(self):
        self.PREFIX = DC_BOT_PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        self.stdin = None
        self.stdout = None
        
        #db.autosave()

        print('Running bot...')
        super().__init__(command_prefix=DC_BOT_PREFIX, owner_ids=OWNER_ID,)

    def run(self):
        with open(TOKEN_PATH, 'r') as token_file:
            self.TOKEN = token_file.read()
        print('Running setup...')
        self.setup()
        super().run(self.TOKEN, reconnect=True)

    def setup(self):
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f'\t{cog} cog loaded.')
        print('Setup complete.')

    async def on_connect(self):
        print('Bot connected.')

    async def on_disconnect(self):
        print('Bot disconnected.')

    async def on_error(self, err: str, *args, **kwargs):
        if err == 'on_command_error':
            channel = args[0]
            await channel.send('Command error.')
        self.stdout.send('An error occured.')
        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass
        elif hasattr(exc, 'original'):
            raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.legit_users = [await self.fetch_user(user_id) for user_id in USERS_IDS]
            self.guild = self.get_guild(SERVER_ID)
            self.stdout = self.get_channel(OUTPUT_CHANNEL_ID)
            self.stdin = self.get_channel(INPUT_CHANNEL_ID)

            # while not self.cogs_ready.all_ready():
            #     await sleep(0.5)

            self.ready = True
            await self.stdin.send('What is my purpouse?')
            print('Bot ready.')
        else:
            print('Bot reconnected.')

    async def on_message(self, message):
        if message.channel == self.stdin and message.author in self.legit_users:
            await self.process_commands(message)
            
bot = I_pass_butter()