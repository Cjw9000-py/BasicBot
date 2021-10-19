import discord
import logging
from discord.ext import commands

log = logging.getLogger(__name__)

class Setup(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name='set-muterole')
    async def set_mute_role(self, ctx, mute_role: discord.Role):
        cursor = self.client.db.cursor()
        try:
            cursor.execute(
                f'INSERT INTO guild_settings (guild_id, mute_role) VALUES ("{ctx.guild.id}", "{mute_role.id}")'
            )
        except Exception:
            cursor.execute(
                f'UPDATE guild_settings SET mute_role = "{mute_role.id}" WHERE guild_id = "{ctx.guild.id}"'
            )
        self.client.db.commit()
        await ctx.send('Mute role was set to ' + mute_role.mention)

    @commands.command(name='set-logging-channel')
    async def set_log_channel(self, ctx, logging_channel: discord.TextChannel):
        cursor = self.client.db.cursor()
        try:
            cursor.execute(
                f'INSERT INTO guild_settings (guild_id, logging_channel) VALUES ("{ctx.guild.id}", "{logging_channel.id}")'

            )
        except Exception:
            cursor.execute(
                f'UPDATE guild_settings SET logging_channel = "{logging_channel.id}" WHERE guild_id = "{ctx.guild.id}"'
            )
        await ctx.send('Logging channel was set to ' + logging_channel.mention)
        self.client.db.commit()

    @commands.command(name='join')
    async def join(self, ctx):
        embed = discord.Embed(title='I can join your discord!', description='Invite me now!')
        embed.set_thumbnail(url=self.client.user.avatar_url_as())
        embed.add_field(name='Invite Link', value=f'https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot')

        await ctx.send(embed=embed)

    @commands.command(name='about')
    async def about(self, ctx):
        embed = discord.Embed(title='About Me', description='A Discord Bot written fully in The Python Programming Language.\n The Source Code is available on Github.\n My Bot was made with love and i hope it can help you!')
        embed.set_thumbnail(url=self.client.user.avatar_url_as())
        embed.set_author(name='Cjw9000#4299', url='https://github.com/Cjw9000-py', icon_url='https://cdn.discordapp.com/avatars/548607822871527454/a43c370b02e109e47b30232aff715606.png')
        embed.add_field(name='Made By', value=f'Discord: {self.client.get_user(self.client.owner_id)}\nGithub: https://github.com/Cjw9000-py', inline=False)
        embed.add_field(name='Github', value='link', inline=False)
        embed.add_field(name='Version', value=self.client.version, inline=True)
        embed.add_field(name='Discord.py Version', value=discord.__version__, inline=True)
        embed.add_field(name='Python', value='https://python.org', inline=False)
        embed.add_field(name='Discord.py', value='readthedocs: https://discordpy.readthedocs.io/en/stable/\nGithub: https://github.com/Rapptz/discord.py\npypi: https://pypi.org/project/discord.py/', inline=True)

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Setup(client))