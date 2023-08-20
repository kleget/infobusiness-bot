from importt import *
# from pay import *

# ГЕНЕРАЦИЯ РАНДОМНОЙ СТРОКИ ДЛЯ УНАКАЛЬНОСТИ КАЖДОГО ПЛАТЕЖА
async def generate_random_string():
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(15))
    return random_string

async def generate_random_code(num):
    e = []
    e.append(lists[random.randint(0, 24)])
    for x in range(5):
        e.append(lists[random.randint(0, 33)])
    return f"{''.join(e)}_{num}"


# ПОЛУЧАЕМ ID АУДИО
@dp.message_handler(content_types=["audio"])
async def get_audio_file(message: types.Message):
    if message.chat.id == 1277447609:
        a = await db_select_one_pole('ras', 'action', ID_ADMIN)
        if a[0] == 'set_audio':
            all_params = await db_select_all_pole('params',  ID_ADMIN)
            all_params = all_params[0][61:81]
            for i in range(len(all_params)):
                if all_params[i] == 'pass':
                    a = str(datetime.timedelta(seconds=int(message.audio.duration)))
                    if a[0] == '0':
                        a = a[2:]
                    if a[0] == '0':
                        a = a[1:]
                    await db_update_one_pole('params', f"audio_{num_dict[i]}", ID_ADMIN, f"{message.audio.file_id}::{a}")
                    break
            await bot.send_message(chat_id=ID_ADMIN, text='Аудио запись добавлена')



