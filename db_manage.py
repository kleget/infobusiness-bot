import sqlite3 as sq

async def db_insert_two_pole(base, pole, id, text):
    with sq.connect(f'db_{base}.db') as con:
        sql = con.cursor()
        # print(f"INSERT INTO {base} ({str(pole), 'chat_id'}) VALUES (?, ?)", (str(text), str(id),))
        sql.execute(f"INSERT INTO {base} {str(pole), 'chat_id', 'work'} VALUES (?, ?, ?)", (str(text), str(id), 'True',))

async def db_update_one_pole(base, pole, id, text):
    with sq.connect(f'db_{base}.db') as con:
        sql = con.cursor()
        sql.execute(f"UPDATE {base} SET {str(pole)} = (?) WHERE chat_id == '{str(id)}'", (str(text),))
        con.commit()

async def db_update_one_pole_where(base, pole, id, param, text):
    with sq.connect(f'db_{base}.db') as con:
        sql = con.cursor()
        sql.execute(f"UPDATE {base} SET {str(pole)} = (?) WHERE chat_id == '{str(id)}' AND code == '{str(param)}'", (str(text),))
        con.commit()

async def db_select_one_pole(base, pole, id):
    with sq.connect(f'db_{base}.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT {str(pole)} FROM {base} WHERE chat_id == '{str(id)}'")
        return sql.fetchone()

async def db_select_all_pole(base, id):
    with sq.connect(f'db_{base}.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM {base} WHERE chat_id == '{str(id)}'")
        return sql.fetchall()
async def inicialization(id):
    with sq.connect(f'db_main.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT chat_id FROM main WHERE chat_id == {str(id)}")
        if sql.fetchone() is None:
            with sq.connect(f'db_main.db') as con:
                sql = con.cursor()
                sql.execute("INSERT INTO main (chat_id, one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen, eighteen, nineteen, twenty, promo_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (str(id), 'False', 'False', 'False', 'False', 'False', 'False', 'False', 'False','False', 'False', 'False', 'False','False', 'False', 'False', 'False','False', 'False', 'False', 'False', 'False',))
        else:
            pass

async def get_rasslika():
    with sq.connect(f'ras.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT rassilka FROM ras")
        return sql.fetchall()

async def update_rasslika(txt):
    with sq.connect(f'ras.db') as conn:
        sql = conn.cursor()
        sql.execute("UPDATE ras SET rassilka = ?", (txt,))
        conn.commit()
