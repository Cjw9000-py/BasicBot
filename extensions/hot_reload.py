import logging
from discord.ext import commands

log = logging.getLogger(__name__)

class HotReload(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        log.info('HotReloading...')
        for ext in self.client.settings.get('extensions', []):
            self.client.reload_extension(ext)
        # await self.client.process_commands(message)


def setup(client):
    client.add_cog(HotReload(client))