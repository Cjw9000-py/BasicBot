import datetime
import logging
import discord
from discord.ext import commands


log = logging.getLogger(__name__)
DEBUG = True

def debug():
    if DEBUG:
        log.info('!!!DEBUG MODE IS ON!!! NO MODERATION ACTIONS WILL BE MADE')
    return DEBUG

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def basic_moderation_check(ctx, user: discord.Member, admin: bool = True):
        author: discord.Member = ctx.author

        if author.guild.owner == author:
            return True
        if author == user:
            await ctx.send('You cannot use this command on yourself!')
            return False
        if user.guild.owner == user:
            await ctx.send('You cannot use this command on the owner!')
            return False
        if user.guild_permissions.administrator and admin:
            await ctx.send('You cannot use this command on a administrator!')
            return False
        return True

    async def get_mute_role(self, ctx):
        res = self.client.db.execute(f'SELECT mute_role FROM guild_settings WHERE guild_id = "{ctx.guild.id}"')
        res = res.fetchall()
        try:
            mute_id = res[0][0]
        except IndexError:
            await ctx.send('No mute role was found please set one with "set-muterole <@role>"')
            log.debug('NO MUTE ROLE FOUND ' + str(ctx.guild.id))
            return

        return [i for i in ctx.guild.roles if i.id == int(mute_id)][0]

    @commands.command(name='ban')
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):
        if not await self.basic_moderation_check(ctx, user):
            log.debug('Moderation check failed on BAN')
            return
        
        if debug():
            await ctx.send('BAN')
        else:
            await user.ban(reason=reason)

    @commands.command(name='kick')
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        if not await self.basic_moderation_check(ctx, user):
            log.debug('Moderation check failed on KICK')
            return
        
        if debug():
            await ctx.send('KICK')
        else:
            await user.kick(reason=reason)

    @commands.command(name='mute')
    @commands.guild_only()
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, user: discord.Member, *, reason: str = None):
        if not await self.basic_moderation_check(ctx, user, False):
            return

        mute_role = await self.get_mute_role(ctx)

        await user.add_roles(mute_role)

        embed = discord.Embed(
            title='Muted ' + user.mention,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name='Reason', value=(reason if reason is not None else 'No reason supplied.'))

        await ctx.send(embed=embed)

    @commands.command(name='move-all')
    @commands.guild_only()
    @commands.has_guild_permissions(move_members=True)
    @commands.bot_has_guild_permissions(move_members=True)
    async def move_all(self, ctx, channel: discord.VoiceChannel, to: discord.VoiceChannel = None):
        if to is None:
            to = channel
            channel = ctx.author.voice_state.channel

        for user_id, state in channel.voice_states.items():
            user = ctx.guild.get_member(user_id)
            await user.move_to(to)

        await ctx.send(f'Moved all members in {channel.mention} to {to.mention}')

    @commands.command(name='unmute')
    @commands.guild_only()
    @commands.has_guild_permissions(mute_members=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, user: discord.Member, *, reason: str = None):
        if not await self.basic_moderation_check(ctx, user):
            return

        mute_role = await self.get_mute_role(ctx)
        await user.remove_roles(mute_role)

        embed = discord.Embed(
            title='Unmuted ' + user.mention,
            timestamp=datetime.datetime.now()
        )
        embed.add_field(name='Reason', value=(reason if reason is not None else 'No reason supplied.'))

        await ctx.send(embed=embed)

    @commands.command(name='unban')
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.Member, *, reason: str = None):
        if not await self.basic_moderation_check(ctx, user):
            return

        if debug():
            await ctx.send('UNBAN')
        else:
            await user.unban(reason=reason)


def setup(client):
    client.add_cog(Moderation(client))