import logging
import discord
import datetime

from discord.ext import commands

log = logging.getLogger(__name__)

class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client

    @staticmethod
    async def get_logging_channel(guild, client):
        res = client.db.execute(
            f'''SELECT logging_channel FROM guild_settings WHERE guild_id = "{guild.id}"'''
        )
        res = res.fetchall()
        try:
            if res[0][0] is None:
                raise IndexError
            channel = client.get_channel(int(res[0][0]))
            return channel
        except IndexError:
            raise NoLoggingChannel

    @staticmethod
    def get_name(user):
        return f'{user.name}#{user.discriminator}'

    @staticmethod
    def get_embed(user, title, desc, *fields):
        embed = discord.Embed(title=title, timestamp=datetime.datetime.now(), description=desc)
        embed.set_thumbnail(url=user.avatar_url_as())
        for i in fields:
            embed.add_field(name=i[0], value=i[1])
        return embed

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = await self.get_logging_channel(message.guild, self.client)

        embed = self.get_embed(
            message.author,
            'Message deleted',
            f'Message deleted in {message.channel.mention}',
            ('Author', self.get_name(message.author)),
            ('Content', message.content)
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = await self.get_logging_channel(before.guild, self.client)

        embed = self.get_embed(
            before.author,
            'Message Edited',
            f'Message edited in {before.channel.mention}',
            ('Author', self.get_name(before.author)),
            ('Before', before.content),
            ('After', after.content)
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        channel = await self.get_logging_channel(message.guild, self.client)

        embed = self.get_embed(
            message.author,
            'Reactions cleared',
            f'{len(reactions)} Reactions cleared in {message.channel.mention}',
            ('Author', self.get_name(message.author)),
            ('Message', message.content)
        )

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_private_channel_delete(self, channel: discord.TextChannel):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Private Channel Deleted',
            f'{channel.mention} was deleted',
            ('Channel', channel.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_private_channel_create(self, channel):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Private Channel Created',
            f'{channel.mention} was created',
            ('Channel', channel.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_private_channel_update(self, before, after):
        log_channel = await self.get_logging_channel(before.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Private Channel updated',
            f'{before.mention} was updated',
            ('Before', before.name),
            ('After', after.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, channel, last_pin):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Private Channel pin update',
            f'{last_pin} as added to pins',
            ('Channel', channel.name),
            ('Pin', last_pin)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Channel Deleted',
            f'{channel.mention} was deleted',
            ('Channel', channel.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Channel Created',
            f'{channel.mention} was created',
            ('Channel', channel.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, channel, last_pin):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Channel Pins Update',
            f'{last_pin} as added to pins',
            ('Channel', channel.name),
            ('Pin', last_pin)

        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_integrations_update(self, guild):
        log_channel = await self.get_logging_channel(guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Guild Integrations Update',
            f'Guild integrations have updated',
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_webhooks_update(self, channel):
        log_channel = await self.get_logging_channel(channel.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Webhooks have Updated',
            f'Webhooks in {channel.mention} have updated',
            ('Channel', channel.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = await self.get_logging_channel(member.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Member joined',
            f'{member.mention} joined',
            ('Member', member.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = await self.get_logging_channel(member.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Member joined',
            f'{member.mention} joined',
            ('Member', member.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = await self.get_logging_channel(before.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Member joined',
            f'{before.mention} joined',
            ('Member', before.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # implement adding guild settings!
        cursor = self.client.db.cursor()
        cursor.execute(f'INSERT INTO guild_settings(guild_id) VALUES ("{guild.id}")')
        self.client.db.commit()
        log.debug(f'ADDED GUILD {guild.id} TO DATABASE')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # implement removing guild settings!
        cursor = self.client.db.cursor()
        cursor.execute(f'DELETE FROM guild_settings WHERE guild_id = "{guild.id}"')
        cursor.execute(f'DELETE FROM moderation_queue WHERE guild_id = "{guild.id}"')
        self.client.db.commit()
        log.debug(f'REMOVED GUILD {guild.id} FROM DATABASE')

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        log_channel = await self.get_logging_channel(before, self.client)

        embed = self.get_embed(
            self.client.user,
            'Guild Update',
            f'This guild updated',
            ('Name', after.name)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        log_channel = await self.get_logging_channel(role.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Role Created',
            f'{role.name} was created',
            ('Role', role.name),
            ('Id', role.id)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        log_channel = await self.get_logging_channel(role.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Role Deleted',
            f'{role.name} was deleted',
            ('Role', role.name),
            ('Id', role.id)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        log_channel = await self.get_logging_channel(before.guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Role Update',
            f'{before.name} was updated',
            ('Role', before.name),
            ('Id', before.id)
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): ...

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = await self.get_logging_channel(guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'Member banned',
            f'{user.name} was banned',
            ('Name', self.get_name(user)),
        )
        await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = await self.get_logging_channel(guild, self.client)

        embed = self.get_embed(
            self.client.user,
            'User unbanned',
            f'{user.name} was unbanned',
            ('Name', self.get_name(user)),
        )
        await log_channel.send(embed=embed)

NoLoggingChannel = type('NoLoggingChannel', (Exception,), {})


def setup(client):
    client.add_cog(Logging(client))