import sqlite3 as sq
db = sq.connect('base.db')
cur = db.cursor()
async def db_start():
    cur.execute("CREATE TABLE IF NOT EXISTS profile(chat_id TEXT PRIMARY KEY, title TEXT, count TEXT)")
    db.commit()


async def chats(chat_id, title, count):
    chat = cur.execute("SELECT 1 FROM profile WHERE chat_id == '{key}'".format(key=chat_id)).fetchone()
    if not chat:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?)", (chat_id, title, count))
        db.commit()


def yea_chats():
    sql = "SELECT title FROM profile"
    cur.execute(sql)
    results = cur.fetchall()
    results = [i[0] for i in results]
    results = (', '.join(results))
    return results
    db.commit()

def id_chats(row_size):
    sql = "SELECT * FROM profile"
    cur.execute(sql)
    results = cur.fetchmany(row_size)
    for row in results:
        id = ('ID:', row[0])
        name = ('Имя:', row[1])
        return name + id
    row = (', '.join(results))
    return row
    db.commit()


async def sql_read(message):
    rows = cur.execute('SELECT * FROM pricec').fetchall()
    text = ""
    for ret in rows:
        text = text + "" + f"{ret[0]}" "-" f"{ret[2]}"
        await bot.send_message(message.chat.id, text)


########
