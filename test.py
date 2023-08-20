# import time
# import time

# from importt import *

# comment = 'seven:841767119:HZnfchJDqV6XR65'
# history = client.operation_history()#label=comment)

# if history.operations == []:
#     print("Сожалеем, но платеж не был обнаружен. Попробуйте еще раз проверить платеж, нажав кнопку снова")
# else:
#     for i in range(len(history.operations)):
#         if history.operations[i].status == 'success':
#             print(i, "   ", history.operations[i].amount)


# from pyrogram import Client as cl
# from db_manage import *
# from time import sleep
# from yoomoney import Client, Quickpay
# import asyncio
# token = "4100117823395070.F2FC9FD26DE9EBD7467BD6625F813A3BDBECC1BF26C7D8087E6909D52BF280CBD3D8645F3FA8AFB492BDB1137F81BB28F610F784F17862A01680DF6CE291EE2460E488BDBEC4ECE0D9B466CB101F21ABEEE0677EE54B3F7640B04435E0A896B450988C77B2C45CFFC2E6A42AA21E8873AF44DF7E847A388D74D935A0D8252F59"
# client = Client(token)
# api_id=26023371
# api_hash='730b80f287f342de7d6f81ab54688c5d'
# app = cl("my_account", api_id=api_id, api_hash=api_hash)
# print('WORK')
#
# app.run()
#
#
# async def send_message():
#     with app:
#         with sq.connect(f'db_paybot.db') as con:
#             sql = con.cursor()
#             sql.execute(f"SELECT * FROM label")
#             bases = sql.fetchall()
#         base = []
#         for i in range(len(bases)):
#             base.append(bases[i][0])
#
#         history = client.operation_history()
#         for i in range(len(history.operations)):
#             if history.operations[i].label not in base or len(base) == 0:
#                 if history.operations[i].label != None:
#                     await app.send_message(chat_id=-1001983428321, text=history.operations[i].label)  # , reply_to_message_id=6)
#                     with sq.connect('db_paybot.db') as con:
#                         sql = con.cursor()
#                         sql.execute("INSERT INTO label (label) VALUES (?)", (history.operations[i].label,))
#                         con.commit()
#
#
# while True:
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(send_message())
#
#     # send_message()
#     sleep(30)

# from pyrogram import Client
# from db_manage import *
#
# api_id=26023371
# api_hash='730b80f287f342de7d6f81ab54688c5d'
#
# app = Client("my_account", api_id=api_id, api_hash=api_hash)
# print('WORK')
#
# @app.on_message()
# async def echo(client, message):
#     if message.chat.id == -1001983428321:
#         t = message.text.split('^')
#         # await db_update(str(t[0]))
#         await app.send_message(chat_id=5473760952, text=t[1])
#     elif message.chat.id == 5473760952:
#         # a = await db_select()
#         try:
#             if message.media.value == 'photo':
#                 await app.send_photo(chat_id=-1001983428321, photo=message.photo.file_id)
#         except:
#             pass
#         if message.text:
#             await app.send_message(chat_id=-1001983428321, text=f"{int(a[0])}^{message.text}")
#
# app.run()
from pyrogram import Client
from db_manage import *
from time import sleep
from yoomoney import Client as cl
from yoomoney import Quickpay
token = "4100117823395070.F2FC9FD26DE9EBD7467BD6625F813A3BDBECC1BF26C7D8087E6909D52BF280CBD3D8645F3FA8AFB492BDB1137F81BB28F610F784F17862A01680DF6CE291EE2460E488BDBEC4ECE0D9B466CB101F21ABEEE0677EE54B3F7640B04435E0A896B450988C77B2C45CFFC2E6A42AA21E8873AF44DF7E847A388D74D935A0D8252F59"
client = cl(token)
api_id=26023371
api_hash='730b80f287f342de7d6f81ab54688c5d'

app = Client("my_account", api_id=api_id, api_hash=api_hash)
print('WORK')

# Создаем клиент Pyrogram
# app = Client("my_bot")

# Обработчик для отправки сообщения каждые 30 секунд
def send_message():
    # with app:
    with sq.connect(f'db_paybot.db') as con:
        sql = con.cursor()
        sql.execute(f"SELECT * FROM label")
        bases = sql.fetchall()
        base = []
        for i in range(len(bases)):
            base.append(bases[i][0])

        history = client.operation_history()
        for i in range(len(history.operations)):
            if history.operations[i].label not in base or len(base) == 0:
                if history.operations[i].label != None and ':' in history.operations[i].label:
                    now = history.operations[i].datetime
                    app.send_message(  # лог покупок
                        chat_id=-1001924145374,
                        text=f"**Сумма:** {history.operations[i].amount} ₽\n**Дата:** {now.strftime('%H:%M   %d.%m.%y')}\n**Комментарий:** #{history.operations[i].label}\n**Operation_id:**{history.operations[i].operation_id}#\n**Статус платежа:** {history.operations[i].status}",reply_to_message_id = 4)#,parse_mode = "markdown")

                    # app.send_message(chat_id=-1001924145374, text=f"**Amount:** {history.operations[0].amount}\n**Date:** {now.strftime('%S.%M.%H %d.%m.%y')}\n**Lable:** {history.operations[i].label}\n**Operation_id:** {history.operations[0].operation_id}", reply_to_message_id=6, parse_mode="markdown")
                    with sq.connect('db_paybot.db') as con:
                        sql = con.cursor()
                        sql.execute("INSERT INTO label (label) VALUES (?)", (history.operations[i].label,))
                        con.commit()


# Запускаем отправку сообщений каждые 30 секунд

# app.run()
def main():
    with app:
        while True:
            try:
                send_message()
                sleep(5)
            except Exception:
                print(Exception)

if __name__ == '__main__':
    main()