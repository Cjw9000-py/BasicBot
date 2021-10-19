import sqlite3, os

# os.system('mv db.sqlite db_backup.sqlite')
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
        member_id VARCHAR(100),
        action INTEGER,
        created VARCHAR(10),
        timeout VARCHAR(10),
        PRIMARY KEY(guild_id)
    )""")
except Exception as e:
    print(e)

cursor = conn.cursor()
try:
    cursor.execute('INSERT INTO guild_settings (guild_id, mute_role, logging_channel) VALUES ("124", "1234", "9123")')
except Exception as e:
    print(e)
conn.commit()

try:
    print(cursor.execute('SELECT * FROM guild_settings').fetchall())
except Exception as e:
    print(e)