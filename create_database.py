import sqlite3, os

os.system('mv db.sqlite db_backup.sqlite') # yes linux is the best
conn = sqlite3.connect('db.sqlite')

try:
    conn.execute(
    """CREATE TABLE guild_settings (
        guild_id VARCHAR(100) NOT NULL,
        mute_role VARCHAR(100) NULL,
        logging_channel VARCHAR(100) NULL,
        PRIMARY KEY(guild_id)
        )"""
    )

    conn.execute(
    """CREATE TABLE moderation_queue (
        guild_id VARCHAR(100) NOT NULL,
        member_id VARCHAR(100) NOT NULL,
        action INTEGER NOT NULL,
        created VARCHAR(10) NOT NULL,
        timeout VARCHAR(10) NULL,
    )""")
except Exception as e:
    print(e)
