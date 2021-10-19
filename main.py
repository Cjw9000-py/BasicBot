import json
import logging
import sqlite3

import discord
from discord.ext import commands

__version__ = '1.0.0b'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class Client(commands.Bot):
    def __init__(self, _settings):
        intents = discord.Intents.all()
        super(Client, self).__init__(command_prefix=_settings.get('prefix'), intents=intents, owner_id=_settings.get('owner', None))
        self.settings = _settings
        self.db = sqlite3.connect(self.settings.get('database', 'db.sqlite'))
        self.version = __version__

    def get_bot_info(self) -> str:
        text = self.user.name + '#' + self.user.discriminator
        text += f' - (ID: {self.user.id})'
        return text

    def load_bot_extensions(self):
        for ext in self.settings.get('extensions', list()):
            try:
                self.load_extension(ext)
                log.info(f'Loaded extension "{ext}" successfully')
            except Exception as e:
                log.warning(f'Error while loading extension "{ext}"', exc_info=e)

    async def on_ready(self):
        log.info('Bot is ready | ' + self.get_bot_info())

    async def on_shard_ready(self, shard_id):
        log.info(f'Shard {shard_id} is ready | ' + self.get_bot_info())

    async def on_connect(self):
        log.info('Bot connected to discord | ' + self.get_bot_info())
        self.load_bot_extensions()

    async def on_shard_connect(self, shard_id):
        log.info(f'Shard {shard_id} connected to discord | ' + self.get_bot_info())

    async def on_disconnect(self):
        log.info('Bot disconnected from discord | ' + self.get_bot_info())

    async def on_shard_disconnect(self, shard_id):
        log.info(f'Shard {shard_id} disconnected from discord | ' + self.get_bot_info())

    async def on_resume(self):
        log.info('Resuming Session | ' + self.get_bot_info())

    async def on_shard_resume(self, shard_id):
        log.info(f'Shard {shard_id} is Resuming... | ' + self.get_bot_info())


if __name__ == '__main__':
    settings = dict()
    try:
        settings: dict = json.load(open('settings.json'))
    except FileNotFoundError as e:
        log.critical('Settings file was not found!', exc_info=e)
        exit(-1)
    except json.JSONDecodeError as e:
        log.critical('Bad Settings file! Correct any errors and retry!', exc_info=e)
        exit(-1)
    except Exception as e:
        log.critical('Error occurred while loading Settings file', exc_info=e)
        exit(-1)

    settings.setdefault('prefix', '!')

    client = Client(settings)
    client.run(settings.get('token'))