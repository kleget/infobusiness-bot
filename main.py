import small_func
from importt import *
from pay import *
from db_manage import *


@dp.message_handler(commands=['start'])
async def start_com(message: types.Message):
    await inicialization(message.chat.id)  # ДОБАВЛЯЕЮ ЮЗЕРА А БД
    await db_update_one_pole('main', 'promo_code', message.chat.id, 'False')
    await bot.send_message(chat_id=-1001924145374,
                           text=f"*chat id:* `{message.chat.id}`\n*link:* {message.chat.mention}\n*msg id:* `{message.message_id}`\n*text:* {message.text}",
                           reply_to_message_id=2, parse_mode="MarkdownV2")
    if message.chat.id == ID_ADMIN:
        s = await db_select_all_pole('params', '1277447609')
        s_name = [i for i in s[0][1:21] if i != 'pass']
        s_price = [i for i in s[0][21:41] if i != 'pass']
        s_text = [i for i in s[0][41:61] if i != 'pass']
        s_audio = [i for i in s[0][61:81] if i != 'pass']
        button_list = [
            types.InlineKeyboardButton(
                text=f"{s_name[x]} ⏳ {s_audio[x].split('::')[1]} {'🎁 ' if s_price[x] == '0' else ''}[{s_price[x]}₽]",
                callback_data=str(f"audio:{num_dict[x]}")
            ) for x in range(len(s_name))
        ]
        link_on_chanel = InlineKeyboardButton('Наш канал', url='https://t.me/audioaptechka')
        support = InlineKeyboardButton('Тех поддержка', callback_data='support')
        question = InlineKeyboardButton('Задать вопрос', callback_data='question')
        offer = InlineKeyboardButton('Сделать предложение', callback_data='offer')
        admin_panel = InlineKeyboardButton('Админка', callback_data='admin_panel')
        keyboard = InlineKeyboardMarkup(row_width=1).add(*button_list, link_on_chanel, support, question, offer, admin_panel)
    else:
        s = await db_select_all_pole('params', '1277447609')
        s_name = [i for i in s[0][1:21] if i != 'pass']
        s_price = [i for i in s[0][21:41] if i != 'pass']
        s_text = [i for i in s[0][41:61] if i != 'pass']
        s_audio = [i for i in s[0][61:81] if i != 'pass']
        button_list = [
            types.InlineKeyboardButton(
                text=f"{s_name[x]} ⏳ {s_audio[x].split('::')[1]} {'🎁 ' if s_price[x] == '0' else ''}[{s_price[x]}₽]",
                callback_data=str(f"audio:{num_dict[x]}")
            ) for x in range(len(s_name))
        ]
        link_on_chanel = InlineKeyboardButton('Наш канал', url='https://t.me/audioaptechka')
        support = InlineKeyboardButton('Тех поддержка', callback_data='support')
        question = InlineKeyboardButton('Задать вопрос', callback_data='question')
        offer = InlineKeyboardButton('Сделать предложение', callback_data='offer')
        keyboard = InlineKeyboardMarkup(row_width=1).add(*button_list, link_on_chanel, support, question, offer)
    await bot.send_message(
        chat_id=message.chat.id,
        text='Выберите аудиотаблетку:',
        reply_markup=keyboard,
        parse_mode="MarkdownV2")


#ОТПРВКА АУДИО ФАЛЙЛА ИЛИ ПРОСЬБО ОПЛАТИТЬ
@dp.callback_query_handler(lambda c: c.data.startswith('audio'))
async def process_callback_pfffffffsd(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_callback_params_any_2(callback_query)

# АДМИН ПАНЕЛЬ
@dp.callback_query_handler(lambda c: c.data.startswith('admin_panel'))
async def process_callback_pdddddd(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    stat = InlineKeyboardButton('Статистика', callback_data='static')
    rasssilka = InlineKeyboardButton('Рассылка', callback_data='rassilka')
    add_audio = InlineKeyboardButton('Добавить аудио запись', callback_data='add_audio')
    manager_promocode = InlineKeyboardButton('Управление промокодами', callback_data='manager_promocode')
    keyb = InlineKeyboardMarkup(row_width=1).add(stat, rasssilka, add_audio, manager_promocode)
    await bot.edit_message_text(chat_id=ID_ADMIN, text='Админка:', reply_markup=keyb, message_id=callback_query.message.message_id)

@dp.callback_query_handler(lambda c: c.data.startswith('support'))
async def process_callback_support(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await db_update_one_pole('main', 'support', callback_query.from_user.id, 'support')
    await bot.send_message(chat_id=callback_query.from_user.id, text='Поддержка на связи. Опишите вашу ситуацию или вопрос, мы решим любой проблему и все объясним. ')

@dp.callback_query_handler(lambda c: c.data.startswith('offer'))
async def process_callback_offer(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await db_update_one_pole('main', 'support', callback_query.from_user.id, 'offer')
    await bot.send_message(chat_id=callback_query.from_user.id, text='Можете сделать любое преложение в виде аудио таблетки, улучшения нашего бота или даже коммерческого')

@dp.callback_query_handler(lambda c: c.data.startswith('question'))
async def process_callback_question(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await db_update_one_pole('main', 'support', callback_query.from_user.id, 'question')
    await bot.send_message(chat_id=callback_query.from_user.id, text='Можете задать любой вопрос гипноаудио терапевту.')


@dp.callback_query_handler(lambda c: c.data.startswith('add_audio'))
async def process_callback_asdf(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(chat_id=ID_ADMIN, text="Введите название для записи:")
    await db_update_one_pole('ras', 'action', ID_ADMIN, 'set_name')

@dp.callback_query_handler(lambda c: c.data.startswith('manager_promocode'))
async def process_callback_manager_code(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    status_promocodes = InlineKeyboardButton('Статус промокодов', callback_data='status_promocodes')
    get_one_code = InlineKeyboardButton('Выдать разовый код', callback_data='get_one_code')
    keyb = InlineKeyboardMarkup(row_width=1).add(status_promocodes, get_one_code)
    await bot.edit_message_text(chat_id=ID_ADMIN, text='Можно изменить статус постоянных промокодов вкл/выкл\nТакже можно выдать разовый промокод одному пользователю', reply_markup=keyb, message_id=callback_query.message.message_id)



@dp.callback_query_handler(lambda c: c.data.startswith('status_promocodes'))
async def process_callback_manager_code(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    s = await db_select_all_pole('params', ID_ADMIN)
    s_name = [i for i in s[0][1:21] if i != 'pass']
    s_price = [i for i in s[0][21:41] if i != 'pass']
    button_list = [
        types.InlineKeyboardButton(
            text=f"{s_name[x]} [{s_price[x]}₽]",
            callback_data=str(f"mng_code_audio_1:{num_dict[x]}")
        ) for x in range(len(s_name))
    ]

    keyboard = InlineKeyboardMarkup(row_width=1).add(*button_list)
    await bot.edit_message_text(chat_id=ID_ADMIN, text='Выберите запись, чтобы управлять промокодами', reply_markup=keyboard, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data.startswith('get_one_code'))
async def process_callback_manager_code(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await db_update_one_pole('ras', 'action', ID_ADMIN, 'get_user_link')
    await bot.edit_message_text(chat_id=ID_ADMIN,
                                text='Отправьте в бота @username_to_id_bot ссылку на пользователя, которому хотите дать промокод.\n'
                                     'бот пришлет ответ, где вам нужно скопировать id в виде 1234567890 и прислать сюда в чат',
                                message_id=callback_query.message.message_id)




@dp.callback_query_handler(lambda c: c.data.startswith('mng_code_audio_1'))
async def process_callback_sdfsa(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    audio = callback_query.data.split(':')

    s = await db_select_all_pole('promocode', ID_ADMIN)
    s_procent = [30, 50, 70, 100]
    s_price = [i for i in s[0][21:41] if i != 'pass']
    button_list = [
        types.InlineKeyboardButton(
            text=f"{s_procent[x]} %",
            callback_data=str(f"mng_code_audio_2:{audio[1]}:{s_procent[x]}")
        ) for x in range(len(s_procent))
    ]

    keyboard = InlineKeyboardMarkup(row_width=1).add(*button_list)

    audi = await db_select_one_pole('params', audio[1], ID_ADMIN)
    await bot.edit_message_text(chat_id=ID_ADMIN, text=audi[0], reply_markup=keyboard, message_id=callback_query.message.message_id)


@dp.callback_query_handler(lambda c: c.data.startswith('mng_code_audio_2'))
async def process_callback_sdfsa(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    audio = callback_query.data.split(':')
    code = codes_2[(num_dict_2[audio[1]]-1)*4 + num_dict_3[int(audio[2])]-1]
    cx = await db_select_one_pole('promocode', f'{audio[1]}_{audio[2]}_promocode', ID_ADMIN)
    audi = await db_select_one_pole('params', audio[1], ID_ADMIN)
    if cx[0] == 'True':
        but = InlineKeyboardButton('Включить ✅', callback_data=f'on:{audio[1]}_{audio[2]}_promocode:{code}:{audio[1]}:{audio[2]}')
    elif cx[0] == 'False':
        but = InlineKeyboardButton('Выключить ❌', callback_data=f'off:{audio[1]}_{audio[2]}_promocode:{code}:{audio[1]}:{audio[2]}')
    keyb = InlineKeyboardMarkup(row_width=1).add(but)

    txt = f'Промокод для записи "*{audi[0]}*" на скидку {audio[2]}%\n`{code}` \n{condition[cx[0]]}'
    await bot.edit_message_text(chat_id=ID_ADMIN, text=txt, reply_markup=keyb, parse_mode='MarkdownV2', message_id=callback_query.message.message_id)



@dp.callback_query_handler(lambda c: c.data.startswith('on'))
async def static_function(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    var = callback_query.data.split(':')
    await db_update_one_pole('promocode', var[1], ID_ADMIN, 'True')
    # on = InlineKeyboardButton('Включить ✅', callback_data=f'on:{var[1]}:{var[2]}')
    off = InlineKeyboardButton('Выключить ❌', callback_data=f'off:{var[1]}:{var[2]}:{var[3]}:{var[4]}:')
    keyb = InlineKeyboardMarkup(row_width=1).add(off)
    audi = await db_select_one_pole('params', var[3], ID_ADMIN)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                text=f'Промокод для записи "*{audi[0]}*" на скидку {var[4]}%\n`{var[2]}`\nПромокод включен ✅',
                                message_id=callback_query.message.message_id,
                                reply_markup=keyb,
                                parse_mode='MarkdownV2')

@dp.callback_query_handler(lambda c: c.data.startswith('off'))
async def static_function(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    var = callback_query.data.split(':')
    await db_update_one_pole('promocode', var[1], ID_ADMIN, 'False')
    on = InlineKeyboardButton('Включить ✅', callback_data=f'on:{var[1]}:{var[2]}:{var[3]}:{var[4]}:')
    # off = InlineKeyboardButton('Выключить ❌', callback_data=f'off:{var[1]}:{var[2]}')
    keyb = InlineKeyboardMarkup(row_width=1).add(on)
    # name = 123#await db_select_one_pole('params', var[1], ID_ADMIN)
    audi = await db_select_one_pole('params', var[3], ID_ADMIN)
    await bot.edit_message_text(chat_id=callback_query.from_user.id,
                                text=f'Промокод для записи "*{audi[0]}*" на скидку {var[4]}%\n`{var[2]}`\nПромокод выключен ❌',
                                message_id=callback_query.message.message_id,
                                reply_markup=keyb,
                                parse_mode='MarkdownV2')


@dp.callback_query_handler(lambda c: c.data.startswith('static'))
async def static_function(callback_query: types.CallbackQuery):
    # await bot.answer_callback_query(callback_query.id)
    # count_users = await db_select_all_pole('main', callback_query.from_user.id)
    # count_users = count_users[0][1:20]
    # all_1 = []
    # all_2 = []
    # all_users = await db_select_id_sys('*') # ВСЯ ИНФА ПРО ПОЛЬЗОВАТЕЛЯ
    #
    # for i in range(len(all_users)):
    #     all_1.append(all_users[i][1])
    #     all_2.append(all_users[i][2])
    #
    # all_1 = all_1.count('True')
    # all_2 = all_2.count('True')
    # sum = ((all_1*5000) + (all_2*1000))
    await bot.send_message(chat_id=callback_query.from_user.id, text=f'Напиши статистику')  # Участников в боте: {len(all_users)}\nПродано на {sum} рублей')


# ЛОФИМ ФОТКУ ДЛЯ РАССЫЛКИ
@dp.message_handler(content_types=["photo"])
async def get_foto(message: types.Message):
    a = await get_rasslika()
    x = 0
    if a[0][0] == 'True':
        sub = await db_select_all_pole('main', 'chat_id')
        for i in range(len(sub)):
            try:
                await bot.send_photo(chat_id=sub[i][0], caption=message.caption, photo=message.photo[-1].file_id)
                # await bot.send_message(chat_id=sub[i][0], text=message.text)
                x += 1
            except:
                pass
        await bot.send_message(chat_id=ID_ADMIN, text=f'Рассылка прошла успешно!\nОтправлено {x} сообщений')
        await update_rasslika('False')


# ОСУЩЕСТВЛЕНИЕ РАССЫЛКИ
@dp.message_handler()
async def ras(message: types.Message):
    a = await db_select_one_pole('ras', 'action', ID_ADMIN)
    sup = await db_select_one_pole('main', 'support', message.chat.id)
    if message.chat.id != -1001924145374:
        await bot.send_message(chat_id=-1001924145374, text=f"*chat id:* `{message.chat.id}`\n*link:* {message.chat.mention}\n*msg id:* `{message.message_id}`\n*text:* {message.text}", reply_to_message_id = 2, parse_mode="MarkdownV2")
    if message.chat.id == -1001924145374:
        await bot.send_message(chat_id=message.reply_to_message.md_text.split('\n')[0].split(' ')[2].split('`')[1],
                               text=message.text,
                               reply_to_message_id=message.reply_to_message.md_text.split('\n')[2].split(' ')[2].split('`')[1])
    elif sup[0] == 'support':
        await bot.send_message(chat_id=-1001924145374, text=f"*chat id:* `{message.chat.id}`\n*link:* {message.chat.mention}\n*msg id:* `{message.message_id}`\n*text:* {message.text}", reply_to_message_id = 13, parse_mode="MarkdownV2")
        await db_update_one_pole('main', 'support', message.chat.id, 'pass')
        await bot.send_message(chat_id=message.chat.id, text='Ваше собщение уже рассматривает служба поддержки. Ожидайте. В течении дня бот пришлет сообщение с ответом.')
    elif sup[0] == 'offer':
        await bot.send_message(chat_id=-1001924145374,
                               text=f"*chat id:* `{message.chat.id}`\n*link:* {message.chat.mention}\n*msg id:* `{message.message_id}`\n*text:* {message.text}",
                               reply_to_message_id=11, parse_mode="MarkdownV2")
        await db_update_one_pole('main', 'support', message.chat.id, 'pass')
        await bot.send_message(chat_id=message.chat.id, text='Спасибо за ваше преложние. В случае чего, мы можем связаться с вами в личных сообщениях или отправить сообщение через бот')
    elif sup[0] == 'question':
        await bot.send_message(chat_id=-1001924145374,
                               text=f"*chat id:* `{message.chat.id}`\n*link:* {message.chat.mention}\n*msg id:* `{message.message_id}`\n*text:* {message.text}",
                               reply_to_message_id=9, parse_mode="MarkdownV2")
        await db_update_one_pole('main', 'support', message.chat.id, 'pass')
        await bot.send_message(chat_id=message.chat.id, text='Сообщенеи уже доставлено гипнотерапевту, в течении дня вам поступит ответ в бот. Ожидайте.')

    elif message.chat.id == ID_ADMIN and a[0] in ['rassilka', 'set_name', 'set_price', 'set_text', 'get_user_link', 'set_procents_for_one_link']:
        if a[0][0] == 'rassilka':
            x = 0
            sub = await db_select_all_pole('params', 'chat_id')
            for i in range(len(sub)):
                try:
                    await bot.send_message(chat_id=sub[i][0], text=message.text)
                    x += 1
                except:
                    pass
            await bot.send_message(chat_id=ID_ADMIN, text=f'Рассылка прошла успешно!\nОтправлено {x} сообщений')
            await update_rasslika('False')
        elif a[0] == 'set_name':
            all_params = await db_select_all_pole('params', ID_ADMIN)
            all_params = all_params[0][1:21]
            for i in range(len(all_params)):
                if all_params[i] == 'pass':
                    await db_update_one_pole('params', num_dict[i], ID_ADMIN, message.text)
                    break
            await bot.send_message(chat_id=ID_ADMIN, text='Введите цену')
            await db_update_one_pole('ras', 'action', ID_ADMIN, 'set_price')
        elif a[0] == 'set_price':
            all_params = await db_select_all_pole('params', ID_ADMIN)
            all_params = all_params[0][21:41]
            for i in range(len(all_params)):
                if all_params[i] == 'pass':
                    await db_update_one_pole('params', f"price_{num_dict[i]}", ID_ADMIN, message.text)
                    break
            await bot.send_message(chat_id=ID_ADMIN, text='Введите описание')
            await db_update_one_pole('ras', 'action', ID_ADMIN, 'set_text')
        elif a[0] == 'set_text':
            all_params = await db_select_all_pole('params', ID_ADMIN)
            all_params = all_params[0][41:61]
            for i in range(len(all_params)):
                if all_params[i] == 'pass':
                    await db_update_one_pole('params', f"text_{num_dict[i]}", ID_ADMIN, message.text)
                    break
            await bot.send_message(chat_id=ID_ADMIN, text='Отправьте аудио')
            await db_update_one_pole('ras', 'action', ID_ADMIN, 'set_audio')
        elif a[0] == 'get_user_link':
            await bot.send_message(chat_id=ID_ADMIN, text='Сколько % скидка будет по промокоду? Введите целое число без других знаков')
            await db_update_one_pole('ras', 'action', ID_ADMIN, 'set_procents_for_one_link')
            await db_update_one_pole('ras', 'user_link', ID_ADMIN, message.text)
        elif a[0] == 'set_procents_for_one_link':
            await db_update_one_pole('ras', 'procent', ID_ADMIN, message.text)
            s = await db_select_all_pole('params', ID_ADMIN)
            s_name = [i for i in s[0][1:21] if i != 'pass']
            s_price = [i for i in s[0][21:41] if i != 'pass']
            button_list = [
                types.InlineKeyboardButton(
                    text=f"{s_name[x]} [{s_price[x]}₽]",
                    callback_data=str(f"get_code_for_user:{num_dict[x]}")
                ) for x in range(len(s_name))
            ]

            keyboard = InlineKeyboardMarkup(row_width=1).add(*button_list)
            await bot.send_message(chat_id=ID_ADMIN, text='Выберите запись для которой должен работать промокод.',reply_markup=keyboard)
            await db_update_one_pole('ras', 'action', ID_ADMIN, 'set_procents_for_one_link')
    else:
        c = await db_select_all_pole('main', message.chat.id)
        yt = await db_select_all_pole('params', message.chat.id)
        code_one_use = await db_select_all_pole('onecode', message.chat.id)
        arr = []
        for i in range(len(code_one_use)):
            arr.append(code_one_use[i][1])
        if '_' not in message.text:
            try:
                status_promocode = await db_select_one_pole('promocode',
                                                            f"{c[0][2]}_{int(codes[message.text] * 100)}_promocode",
                                                            message.chat.id)
                if c[0][1] == 'True' and message.text in codes_2 and status_promocode[0] == 'True':
                    await ras_2(message, c[0][2])
                elif status_promocode[0] == 'False':
                    await bot.send_message(chat_id=message.chat.id,
                                           text='Промокод сейчас не активен. Им можно воспользоваться когда объявлят скидку по нему.')
                elif c[0][1] == 'True':
                    await bot.send_message(chat_id=message.chat.id,
                                           text='Неверный промокод. Попробуйте еще раз или оплатите без промокода.')
                else:
                    pass
            except:
                await bot.send_message(chat_id=message.chat.id,
                                       text='Неверный промокод. Попробуйте еще раз или оплатите без промокода.')

        elif c[0][1] == 'True' and message.text in arr:
            for i in range(len(code_one_use)):
                if code_one_use[i][1] == message.text and code_one_use[i][2] == 'True':
                    await ras_4(message, c[0][2])
                    break


@dp.callback_query_handler(lambda c: c.data.startswith('rassilka'))
async def rasilca_function(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # sub = await db_select_id_sys('chat_id')
    await update_rasslika('True')
    back = InlineKeyboardButton('Отменить рассылку', callback_data='back')
    keyb = InlineKeyboardMarkup(row_width=1).add(back)
    await bot.send_message(chat_id=ID_ADMIN, text='Отправьте сообщение в чат и оно придёт всем пользователям бота. Поддерживаемые форматы: текст и картинка', reply_markup=keyb)


@dp.callback_query_handler(lambda c: c.data.startswith('get_code_for_user'))
async def get_code_for_user_func(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # var = callback_query.data.split(':')
    # await update_rasslika('True')
    # back = InlineKeyboardButton('Отменить рассылку', callback_data='back')
    # keyb = InlineKeyboardMarkup(row_width=1).add(back)
    a = await db_select_all_pole('ras', ID_ADMIN)
    e = []
    for x in range(6):
        e.append(lists[random.randint(0, 24)])
    c = f"{''.join(e)}_{a[0][3]}%"
    await db_insert_two_pole('onecode', 'code', a[0][2], c)
    name = await db_select_one_pole('params', callback_query.data.split(":")[1], ID_ADMIN)
    await bot.send_message(chat_id=ID_ADMIN, text=f'Ваш промокод на скидку {a[0][3]}% для записи {name[0]} доступный для пользователя {a[0][2]}\n\n`{c}`', parse_mode="MarkdownV2")
    await db_update_one_pole('ras', 'action', ID_ADMIN, 'pass')



# ОТЛАВЛИВАНИЕ НАЖАНИЯ КНОПКИ НАЗАД ПРИ ВЫБОРЕ РАССЫЛКИ
@dp.callback_query_handler(lambda c: c.data.startswith('back'))
async def process_callback_back(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await update_rasslika('False')
    await bot.send_message(chat_id=callback_query.from_user.id, text='Рассылка отменена')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)