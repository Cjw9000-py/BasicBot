import datetime
import sqlite3
import logging

log = logging.getLogger(__name__)

class DatabaseHandler:
    def __init__(self, filename):
        self.db = sqlite3.connect(filename)


    def set_logging_channel(self, guild_id, channel_id):
        cursor = self.db.cursor()
        cursor.execute(f'UPDATE guild_settings SET logging_channel = "{channel_id}" WHERE guild_id = "{guild_id}"')
        self.db.commit()
        log.debug(f'SET LOGGING_CHANNEL FOR {guild_id}, {channel_id}')

    def set_mute_role(self, guild_id, role_id):
        cursor = self.db.cursor()
        cursor.execute(f'UPDATE guild_settings SET mute_role = "{role_id}" WHERE guild_id = "{guild_id}"')
        self.db.commit()
        log.debug(f'SET MUTE_ROLE FOR {guild_id} {role_id}')

    def get_logging_channel(self, guild_id):
        cursor = self.db.cursor()
        res = cursor.execute(f'SELECT logging_channel FROM guild_settings WHERE guild_id = "{guild_id}"').fetchall()
        try:
            if res[0][0] is None:
                raise IndexError
        except IndexError:
            raise NoLoggingChannel

        return int(res[0][0])

    def get_mute_role(self, guild_id):
        cursor = self.db.cursor()
        res = cursor.execute(f'SELECT mute_role FROM guild_settings WHERE guild_id = "{guild_id}"').fetchall()
        try:
            if res[0][0] is None:
                raise IndexError
        except IndexError:
            raise NoMuteRole
        return int(res[0][0])

    # --- after update ---

    def _parse_time(self, data): ...

    @staticmethod
    def _parse_timeout(timeout):
        if timeout is None:
            timeout = 'NULL'
        else:
            timeout = f'"{timeout}"'
        return timeout


    def add_to_moderation_queue(self, guild_id, member_id, action, timeout=None):
        timeout = self._parse_timeout(timeout)

        cursor = self.db.cursor()
        cursor.execute(f'''INSERT INTO moderation_queue (guild_id, member_id, action, created, timeout) VALUES (
                        "{guild_id}", "{member_id}", {action}, "{str(datetime.datetime.now())}", {timeout}
                       )''')
        self.db.commit()

    def remove_from_moderation_queue(self, guild_id, member_id, created, action, timeout=None): ...



NoLoggingChannel = type('NoLoggingChannel', (Exception,), {})
NoMuteRole = type('NoMuteRole', (Exception,), {})