from datetime import datetime
from math import dist
from dateparser import parse
from lib.bot import USERS_IDS
from lib.bot import bot
from discord.ext.commands import Cog, command, Context
from typing import Dict, List
from apscheduler.triggers.cron import CronTrigger

from random import choice

# Repeated task params:
#   id={string}
#   start={YYYY/MM/DD} (ISO 8601)
#   dayofweek={0-6}
#   day={1-31}
#   week={1-53}
#   who={Bruno, Martin, Stano, Marek}
#   task={string}


class Tasks(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        
        # TODO: prejdi databazu a schedulnni vsetko co treba
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('tasks')
            
    @command(name="repeated_remainder")
    async def repeated_remainder(self, ctx: Context, *, params: str):
        
        # TODO:
        # parse args throw error if something wrong
        task_params = self.parse_repeated_task_params(params)
        # add record to database
        
        bot.scheduler.add_job(self.task_reminder, 'cron', kwargs=task_params, id=task_params['id'], trigger_args=self.get_cron_args(task_params))
        return
    
    async def get_cron_args(task_params: dict) -> dict:
        return {
            'start_date': task_params.get('start', datetime.now()),
            'day_of_week' : task_params.get('dayofweek', None),
            'day' : task_params.get('day', None),
            'week' : task_params.get('week', None)
        }
    
    async def parse_repeated_task_params(self, params: str) -> dict:
        task_data = dict()
        parsed_params = params.split('\n')
        for param in parsed_params:
            name, value = param.split('=')
            if not self.valid_task_param(name, value):
                raise Exception('Invalid parameter:', name, '=', value)
            task_data[name.strip()] = value.strip()
        return task_data
    
    async def valid_task_param(self, name: str, value: str) -> bool:
        # not essential if we aren't stupid (if bored ... code it)
        valid_names = {'id', 'start', 'week', 'dayofweek', 'day', 'who', 'task'}
        # mozno by bodla kontrola mien v who
        return name in valid_names
    
    async def task_reminder(self, **task_data):
        task_embed, tnail = await self.create_bet_embed_base('Task reminder:')
        task_embed.add_field(name='ID:', value=task_data['id'], inline=True)
        task_embed.add_field(name='Description:', value=task_data['task'], inline=True)
        task_embed.add_field(name='Next reminder:', value=bot.scheduler.get_job(task_data['id']).next_run_time, inline=True)
        
        await self.bot.stdout.send(embed=task_embed)
        await self.bot.stdout.send(self.get_mention_message(task_data['who'].split(',')))
        
    async def get_mention_message(self, real_names: List[str]) -> str:
        mention_message = ''
        for name in real_names:
            user_id = USERS_IDS.get(name, None)
            if user_id is not None:
                mention_message += ' | ' + await self.bot.get_user(user_id).mention
                
    
    @command(name="cancel_task")
    async def cancel_task(self, ctx: Context, task_id: int):
        # TODO:
        # cancel scheduled job
        task_info = bot.scheduler.get_job(task_id).name
        bot.scheduler.remove_job(task_id)
        # delete task from database
        await bot.stdout.send('Job with id : ', task_id, ' | task_info :', task_info, ' was removed.')
    
    @command(name="ahoj")
    async def say_hello(self, ctx: Context, task_id: int):
        POZDRAV = [
            "Choď dopiče ty žochár vyjebaný",
            "Rumpel kokotský nehaj ma spať",
            "MRAVCE CHODIA PO BYTE, DOPIČEEE"
            ]
        await bot.stdout.send( choice( POZDRAV ) )
    
def setup(bot):
    bot.add_cog(Tasks(bot))
