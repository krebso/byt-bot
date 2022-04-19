from lib.bot import bot
from discord.ext.commands import Cog, command, Context
from typing import List

class Tasks(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_tasks_ids: List[str] = []

    @Cog.listener()
    async def on_ready(self):
        
        # TODO: prejdi databazu a schedulnni vsetko co treba
        
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up('tasks')
            
    @command(name="repeated_remainder")
    async def repeated_remainder(self, ctx: Context, *, params: str):
        
        # TODO:
        # parse args throw error if something wrong
        await self.parse_repeated_task_params(params)
        # add record to database
        # schedule job : bot.scheduler.add_job(func, 'cron', ... ,start_date="...", end_date="...",id="meno tasku")
        # add job name to active_tasks
        return
    
    async def parse_repeated_task_params(params: str):
        return
    
    @command(name="cancel_task")
    async def cancel_task(self, ctx: Context, task_id: int):
        # TODO:
        # cancel scheduled job
        # delete task from database
        return
    
def setup(bot):
    bot.add_cog(Tasks(bot))