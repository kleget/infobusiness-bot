from importt import *
from small_func import *

# ПРОСТО ПРОМОКОД
async def ras_2(message, audio_indx):
    price = await db_select_one_pole('params', f'price_{audio_indx}', message.chat.id)
    pay_link = InlineKeyboardButton(f'Оплатить со скидкой {int(codes[message.text] * 100)}%',
                                    url=await pay_method(message.chat.id,
                                                         (int(price[0]) * (1 - (codes[message.text]))), audio_indx))
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Вы применили промокод на скидку {int(codes[message.text] * 100)}%!')
    if codes[message.text] == 1.0:
        await db_update_one_pole('main', audio_indx, message.chat.id, 'True')
        await db_update_one_pole('main', 'promo_code', message.chat.id, 'False')
        file_audio_id = await db_select_one_pole('params', f'audio_{audio_indx}', message.chat.id)
        await bot.send_audio(chat_id=message.chat.id, audio=(file_audio_id[0]).split("::")[0], protect_content=True)
    else:
        keyboard_button = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(message.chat.id, text='Чтобы получить доступ к аудиозаписи, нажмите "Оплатить"',
                               reply_markup=keyboard_button, protect_content=True)
        pay_link = InlineKeyboardButton('Я оплатил (а)', callback_data=f'check_pay_status:{audio_indx}:{int(codes[message.text] * 100)}:False:None')
        keyboard_button_2 = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(message.chat.id, text="После оплаты нажмите кнопку, чтобы проверить статус оплаты.",
                               reply_markup=keyboard_button_2, protect_content=True)
        await db_update_one_pole('main','promo_code', message.chat.id, 'False')


# ПРИ ПРОМОКОДЕ СГЕНЕНИРОВАННОМ ДЛЯ 1 ПОЛЬЗОВАТЕЛЯ
async def ras_4(message, audio_indx):
    price = await db_select_one_pole('params', f'price_{audio_indx}', message.chat.id)
    # params = await db_select_all_pole('params', f"price{audio_indx}")
    pay_link = InlineKeyboardButton(f'Оплатить со скидкой {message.text.split("_")[1]}',
                                    url=await pay_method(message.chat.id,
                                                         (int(price[0])*((100 - int(message.text.split("_")[1][:-1])))/100), audio_indx))
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Вы применили промокод на скидку {message.text.split("_")[1]} !')
    if message.text.split("_")[1][:-1] == '100':
        await db_update_one_pole('main', audio_indx, message.chat.id, 'True')
        await db_update_one_pole('main', 'promo_code', message.chat.id, 'False')
        file_audio_id = await db_select_one_pole('params', f'audio_{audio_indx}', message.chat.id)
        await db_update_one_pole('onecode', 'work', message.chat.id, 'False')
        await bot.send_audio(chat_id=message.chat.id, audio=(file_audio_id[0]).split("::")[0], protect_content=True)
    else:
        keyboard_button = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(message.chat.id, text='Чтобы получить доступ к аудиозаписи, нажмите "Оплатить"',
                               reply_markup=keyboard_button, protect_content=True)
        pay_link = InlineKeyboardButton('Я оплатил (а)', callback_data=f'check_pay_status:{audio_indx}:{int(message.text.split("_")[1][:-1])}:True:{message.text}')
        keyboard_button_2 = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(message.chat.id, text="После оплаты нажмите кнопку, чтобы проверить статус оплаты.",
                               reply_markup=keyboard_button_2, protect_content=True)
        await db_update_one_pole('main','promo_code', message.chat.id, 'False')


async def process_callback_params_any_2(callback_query):
    audio = callback_query.data.split(':')
    au = await db_select_one_pole('params', f'price_{audio[1]}', callback_query.from_user.id)
    if au[0] != '0':
        a = await db_select_one_pole('main', audio[1], callback_query.message.chat.id)
        if a[0] == 'True':  # ЕСЛИ УЖЕ ОПЛАЧЕНО, ТО ВЫСЫЛАЕТСЯ АУДИО
            # await db_update_one_pole('params', audio_indx, callback_query.from_user.id, 'True')
            # await db_update_one_pole('main', 'promo_code', callback_query.from_user.id, 'False')
            file_audio_id = await db_select_one_pole('params', f'audio_{audio[1]}', callback_query.from_user.id)
            await bot.send_audio(chat_id=callback_query.from_user.id, audio=
            file_audio_id[0].split("::")[0],
                                 protect_content=True)
        else:  # ОТПРАВКА ССЫЛКИ НА ОПЛАТУ
            pay_link = InlineKeyboardButton('Перейти к оплате', callback_data=f'go_pay:{audio[1]}:False')
            send_promocode = InlineKeyboardButton('Ввести промокод', callback_data=f'send_promocode')
            keyb = InlineKeyboardMarkup(row_width=1).add(pay_link, send_promocode)
            await db_update_one_pole('main', 'audio', callback_query.from_user.id, audio[1])
            text = await db_select_one_pole('params', f'text_{audio[1]}', callback_query.from_user.id)
            await bot.send_message(chat_id=callback_query.message.chat.id, text=text[0], reply_markup=keyb)
            # await db_update_sys('promo_code', callback_query.from_user.id, 'True')
            # await bot.send_message(chat_id=callback_query.message.chat.id, text='Если у вас есть промокод, то отправьте его в чат, если нет, то нажмите на кнопку.', reply_markup=keyb)
            await db_update_one_pole('main', 'audio', callback_query.from_user.id, audio[1])
    else:
        audio_id = await db_select_one_pole('params', f'audio_{audio[1]}', callback_query.from_user.id)
        audio_id = audio_id[0]
        audio_id = audio_id.split('::')
        audio_text = await db_select_one_pole('params', f'text_{audio[1]}', callback_query.from_user.id)
        await bot.send_audio(chat_id=callback_query.message.chat.id, audio=audio_id[0],  caption=audio_text[0], protect_content=True)  # , protect_content=True) #caption=f'Аудио записть : {audio[1]}',



# ЛОВИТ НАЖАТИЕ КНОПКИ ПЕРЕЙТИ К ОПЛАТЕ
@dp.callback_query_handler(lambda c: c.data.startswith('go_pay'))
async def process_callback_go_pay(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    data = callback_query.data.split(':')
    await db_update_one_pole('main','promo_code', callback_query.from_user.id, 'False')
    price = await db_select_one_pole('params', f'price_{data[1]}', callback_query.from_user.id)
    if data[2] == 'one_code':
        pay_link = InlineKeyboardButton('Оплатить', url=await pay_method(callback_query.from_user.id, price[0], data[1]))
        keyboard_button = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(callback_query.message.chat.id,
                               text='Чтобы получить доступ к аудиозаписи, нажмите "Оплатить"',
                               reply_markup=keyboard_button,
                               protect_content=True)

        pay_link = InlineKeyboardButton('Я оплатил (а)', callback_data=f'check_pay_status:{data[1]}:100:False:False')
        keyboard_button_2 = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(callback_query.message.chat.id,
                               text="После оплаты нажмите кнопку, чтобы проверить статус оплаты. ",
                               reply_markup=keyboard_button_2, protect_content=True)
    else:
        pay_link = InlineKeyboardButton('Оплатить',
                                        url=await pay_method(callback_query.from_user.id, price[0], data[1]))
        keyboard_button = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(callback_query.message.chat.id,
                                           text='Чтобы получить доступ к аудиозаписи, нажмите "Оплатить"',
                                           reply_markup=keyboard_button,
                                           protect_content=True)

        pay_link = InlineKeyboardButton('Я оплатил (а)', callback_data=f'check_pay_status:{data[1]}:100:False:False')
        keyboard_button_2 = InlineKeyboardMarkup(row_width=1).add(pay_link)
        await bot.send_message(callback_query.message.chat.id,
                               text="После оплаты нажмите кнопку, чтобы проверить статус оплаты. ",
                               reply_markup=keyboard_button_2, protect_content=True)

# ГЕНЕРАЦИЯ ССЫЛКИ ДЛЯ ОПЛАТЫ
async def pay_method(chat_id, num, audio_num):
    chek_pay_str = f"{audio_num}:{chat_id}:{await generate_random_string()}"
    await bot.send_message(chat_id=-1001924145374, text=chek_pay_str, reply_to_message_id=6)
    await db_update_one_pole('main',  f"{audio_num}_link", chat_id, chek_pay_str)
    link_on_pay = Quickpay(receiver=token.split(".")[0],
                        quickpay_form="shop",
                        targets="Sponsor this project",
                        paymentType="rub",
                        sum=num,
                        label=chek_pay_str)
    return link_on_pay.redirected_url

# ЛОВИТ НАЖАТИЕ КНОПКИ ОТПРАВИТЬ ПРОМОКОД
@dp.callback_query_handler(lambda c: c.data.startswith('send_promocode'))
async def process_callback_send_promocode(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # data = callback_query.data.split(':')
    await db_update_one_pole('main','promo_code', callback_query.from_user.id, 'True')
    # await db_update_sys('promo_code', callback_query.from_user.id, 'False')
    await bot.send_message(callback_query.message.chat.id,
                           text="Введите промокод с учетом регистра",
                           protect_content=True)


#   ЛОВИМ НАЖАТИЕ КНОПКИ ДЛЯ ПРОВЕРКИ ПЛАТЕЖА
@dp.callback_query_handler(lambda c: c.data.startswith('check_pay_status'))
async def process_callback_check_pay_status(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ch_pay = callback_query.data.split(':')
    await check_pay(callback_query, ch_pay[1], callback_query.from_user.mention, ch_pay[3], ch_pay[4])

# ПРОВЕРКА ОПЛАТЫ
async def check_pay(callback_query, num, user_link, one_code, promocode):
    comment = await db_select_one_pole('main', f"{num}_link", callback_query.from_user.id)
    try:
        history = client.operation_history(label=str(comment[0]))
        if history.operations == []:
            await bot.send_message(chat_id=callback_query.from_user.id, text="Сожалеем, но платеж не был обнаружен. Попробуйте еще раз проверить платеж, нажав кнопку снова")
        else:
            for operation in history.operations:
                if operation.status == 'success':
                    if one_code == 'True':
                        await db_update_one_pole_where('onecode', 'work', callback_query.from_user.id, promocode, 'False')
                        await db_update_one_pole('main', num, callback_query.from_user.id, 'True')
                        await bot.send_message(chat_id=ID_ADMIN,
                                               text=f'{user_link} заплатил(а)')  # {history.operations[0].amount} рублей')#int(prices[num]*(1-(int(procents)/100)))
                        # callback_query.data = callback_query.data.split()
                        await process_callback_params_any_2(callback_query)
                    else:
                        await db_update_one_pole('main', num, callback_query.from_user.id, 'True')
                        await bot.send_message(chat_id=ID_ADMIN,
                                               text=f'{user_link} заплатил(а)')  # {history.operations[0].amount} рублей')#int(prices[num]*(1-(int(procents)/100)))
                        await process_callback_params_any_2(callback_query)
    except Exception as e:
        print(e)
