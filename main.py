import telegram
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import ReplyKeyboardRemove
import asyncio
import random
import openai

# Список пользователей, которым разрешено общаться между собой
# Можно добавить свои айди пользователей, разделив их запятой

# Словарь для хранения активных чатов между пользователями
active_chats = {}
free_id = []


async def start(update, context):
    buttons = [
        [KeyboardButton('/connect')],
        [KeyboardButton('/rules')]
    ]

    # Создаем разметку клавиатуры с кнопками
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    """Отправляет приветственное сообщение при запуске бота"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="""Привет! Я бот для анонимного общения и знакомств. Моя цель - помочь людям общаться друг с другом анонимно, а в случае успешного общения - обменяться контактами и узнать друг о друге побольше.

Как это работает?
1. Нажмите кнопку "Подключиться" (/connect), чтобы начать поиск собеседника.
2. Когда мы найдём вам собеседника, вы сможете общаться с ним анонимно через меня.
3. Если вам понравился собеседник и вы хотите продолжить общение за пределами анонимности, вы можете обменяться контактами.

Важно помнить, что во время анонимного общения ваше настоящее имя и контактные данные не раскрываются. Пожалуйста, соблюдайте уважение к собеседнику и не делитесь личной информацией, если не чувствуете уверенности.

Настоятельно рекомендуем ознакомиться с правилами общения (/rules).

Чтобы начать общение, просто нажмите кнопку "Подключиться" (/connect) и ожидайте, пока мы найдём вам собеседника. Если вам не удалось найти подходящего собеседника или вы хотите завершить текущую беседу, используйте команду "/disconnect".

Желаем вам интересных и приятных разговоров!

Если у вас возникли вопросы или проблемы, обратитесь к команде поддержки, написав на почту rtalking_bot@telegram.org.
""", reply_markup=reply_markup)

def generate_chat_response(message):
    openai.api_key = "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"
    intro = "Кратко ответь на это сообщение, представляя, что ты - человек: "
    prompt = "Вопрос: " + intro + message + "\nОтвет:"
    response = openai.Completion.create(
        engine="text-davinci-003",  # Используем gpt3.5-turbo
        prompt= prompt,
        max_tokens=400,  # Максимальное количество токенов в ответе
        n=1,  # Количество вариантов ответов, которые следует сгенерировать
        stop=None,  # Опциональная фраза, которая прекратит генерацию ответа
        temperature=0.7,  # Управляет случайностью ответа (0.0 - наиболее жесткий, 1.0 - наиболее случайный)
        top_p=1.0,
        # Управляет сэмплированием ответа (1.0 - сэмплирование на основе вероятностей, 0.0 - равномерное сэмплирование)
        frequency_penalty=0.0,
        # Управляет предпочтением повторения или разнообразия фраз (0.0 - более однообразные, 1.0 - более разнообразные)
        presence_penalty=0.6
        # Управляет предпочтением использования ранее заданных фраз (0.0 - отсутствие предпочтения, 1.0 - максимальное предпочтение)
    )
    return response.choices[0].text.strip()

async def rules(update, context):
    """Отправляет правила"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="""Правила общения:
1. Будьте вежливы и уважайте других участников. Оскорбления, ненормативная лексика и любые формы дискриминации запрещены.
2. Соблюдайте анонимность. Не раскрывайте личную информацию о себе или других участниках беседы без их согласия.
3. Не размещайте контент, который может быть оскорбительным, непристойным или нарушать законы. Запрещены ссылки на нелегальный контент и пропаганда насилия.
4. Запрещено спамить, отправлять массовые сообщения или нежелательную рекламу.
5. Не призывайте к нарушению законов или вредным действиям.
6. Если вы чувствуете, что нарушаются правила или сталкиваетесь с неподходящим поведением, сообщите об этом администратору бота.

Общаясь через нашего бота, вы соглашаетесь с соблюдением данных правил. Администраторы имеют право предпринять меры, включая блокировку пользователей, при нарушении этих правил.


Спасибо за понимание и приятных разговоров!
""")


async def connect(update, context):
    if update.effective_user.id in active_chats or get_key(update.effective_user.id) in active_chats:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='В уже находитесь в чате \n'
                                            'Используйте /disconnect для отключения', reply_markup=ReplyKeyboardRemove())
    elif free_id == [] or free_id[0] == update.effective_user.id and update.effective_user.id not in free_id:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Ожидайте, пока мы найдём собеседника', reply_markup = ReplyKeyboardRemove())
        nr = random.randint(0, 7)
        user_id = update.effective_user.id
        if nr == 2 or nr == 5:
            active_chats[user_id] = "000000000"
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Собеседник найден, напишите сообщение \n'
                                                'Введите /disconnect для поиска другого человека', reply_markup = ReplyKeyboardRemove())
            print(active_chats)
        else:
            free_id.append(user_id)
            print(free_id)
    elif update.effective_user.id in free_id:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы уже в очереди, не торопитесь \n'
                                            'Ищем для вас лучшего собеседника', reply_markup = ReplyKeyboardRemove())
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Собеседник найден, напишите сообщение \n'
                                            'Введите /disconnect для поиска другого человека', reply_markup = ReplyKeyboardRemove())

        user_id = update.effective_user.id
        print(free_id)
        id = random.randint(0, len(free_id)-1)
        user2_id = free_id[id]
        free_id.pop(id)
        active_chats[user_id] = user2_id
        print(active_chats)
        await context.bot.send_message(chat_id=user2_id,
                                       text='Собеседник найден, напишите сообщение')
    application.add_handler(get_message)
    application.add_handler(voice_handler)
    application.add_handler(video_handler)
    application.add_handler(photo_handler)
    application.add_handler(sticker_handler)
    application.add_handler(disconnect_handler)



def get_key(val):
    for key, value in active_chats.items():
        if val == value:
            return key


async def messages(update, context):
    user_id = update.effective_user.id
    if user_id in active_chats:
        message = update.message
        user2_id = active_chats[user_id]
        if user2_id == "000000000":
            mess2 = generate_chat_response(str(message.text))
            print(mess2)
            await context.bot.send_message(chat_id=user_id, text=mess2)
        else:
            await context.bot.send_message(chat_id=user2_id, text=message.text)
    elif user_id in active_chats.values():
        message = update.message
        user2_id = get_key(user_id)
        await context.bot.send_message(chat_id=user2_id,
                                       text=message.text)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не состоите в переписке')

async def send_photo(update, context):
    """Отправляет фото в чат"""
    user_id = update.effective_user.id
    if user_id in active_chats:
        photo = update.message.photo[-1].file_id
        user2_id = active_chats[user_id]
        await context.bot.send_photo(chat_id=user2_id, photo=photo)
    elif user_id in active_chats.values():
        photo = update.message.photo[-1].file_id
        user2_id = get_key(user_id)
        await context.bot.send_photo(chat_id=user2_id, photo=photo)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не состоите в переписке')


async def send_video(update, context):
    """Отправляет видео в чат"""
    user_id = update.effective_user.id
    if user_id in active_chats:
        video = update.message.video.file_id
        user2_id = active_chats[user_id]
        await context.bot.send_video(chat_id=user2_id, video=video)
    elif user_id in active_chats.values():
        video = update.message.video.file_id
        user2_id = get_key(user_id)
        await context.bot.send_video(chat_id=user2_id, video=video)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не состоите в переписке')


async def send_sticker(update, context):
    """Отправляет стикер в чат"""
    user_id = update.effective_user.id
    if user_id in active_chats:
        sticker = update.message.sticker.file_id
        user2_id = active_chats[user_id]
        await context.bot.send_sticker(chat_id=user2_id, sticker=sticker)
    elif user_id in active_chats.values():
        sticker = update.message.sticker.file_id
        user2_id = get_key(user_id)
        await context.bot.send_sticker(chat_id=user2_id, sticker=sticker)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не состоите в переписке')


async def send_voice(update, context):
    """Отправляет голосовое сообщение в чат"""
    user_id = update.effective_user.id
    if user_id in active_chats:
        voice = update.message.voice.file_id
        user2_id = active_chats[user_id]
        await context.bot.send_voice(chat_id=user2_id, voice=voice)
    elif user_id in active_chats.values():
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не можете отправлять голосовые сообщения в этой переписке')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы не состоите в переписке')

async def exit(update, context):
    """Отправляет правила"""
    buttons = [
        [KeyboardButton('/connect')],
        [KeyboardButton('/rules')]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    user_id = update.effective_chat.id
    if user_id not in free_id and user_id not in active_chats and user_id not in active_chats.values():
        await context.bot.send_message(chat_id=user_id,
                                       text='Вы не состоите в очереди и не находитесь в диалоге.')
    elif user_id in active_chats or user_id in active_chats.values():
        await context.bot.send_message(chat_id=user_id,
                                       text='Вы находитесь в диалоге. \n Используйте /disconnect, чтобы выйти из диалога')
    else:
        if user_id in free_id:
            free_id.remove(user_id)
        await context.bot.send_message(chat_id=user_id,
                                       text='Мы Вас больше не беспокоим!', reply_markup=reply_markup)


async def disconnect(update, context):
    if free_id == []:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы вышли из диалога, ожидайте, пока мы найдём нового собеседника.\n'
                                            'Используйте /exit, если не хотите искать собеседника')
        user_id = update.effective_user.id
        if user_id in active_chats:
            user2_id = active_chats[user_id]
            free_id.append(user_id)
            free_id.append(user2_id)
            print(free_id)
            del active_chats[user_id]
            await context.bot.send_message(chat_id=user2_id,
                                       text='Собеседник вышел из диалога, ожидайте, пока мы найдём нового собеседника.\n'
                                            'Используйте /exit, если не хотите искать собеседника')
        else:
            user2_id = get_key(user_id)
            user_id = active_chats[user_id]
            free_id.append(user_id)
            free_id.append(user2_id)
            del active_chats[user2_id]
            await context.bot.send_message(chat_id=user2_id,
                                           text='Собеседник вышел из диалога, ожидайте, пока мы найдём нового собеседника.\n'
                                                'Используйте /exit, если не хотите искать собеседника')

        print(free_id)
        if user_id in active_chats:
            active_chats.pop(user_id)
        else:
            user2_id = get_key(user_id)
            active_chats.pop(user2_id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Собеседник найден, напишите сообщение')

        user_id = update.effective_user.id
        print(free_id)
        id = random.randint(0, len(free_id)-1)
        if id != user_id:
            user2_id = free_id[id]
            free_id.pop(id)
            active_chats[user_id] = user2_id
            print(active_chats)
            await context.bot.send_message(chat_id=user2_id,
                                           text='Собеседник найден, напишите сообщение')


if __name__ == '__main__':
    TOKEN = '5727519972:AAF5ikBXNPaWr0ogRehK2D-xMZ1Csuhnvzg'

    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    exit_handler = CommandHandler('exit', exit)
    rules_handler = CommandHandler('rules', rules)
    connect_handler = CommandHandler('connect', connect)
    disconnect_handler = CommandHandler('disconnect', disconnect)
    # регистрируем обработчик в приложение
    application.add_handler(rules_handler)
    application.add_handler(exit_handler)
    application.add_handler(connect_handler)
    application.add_handler(disconnect_handler)

    get_message = MessageHandler(filters.TEXT, messages)
    photo_handler = MessageHandler(filters.PHOTO, send_photo)
    video_handler = MessageHandler(filters.VIDEO, send_video)
    sticker_handler = MessageHandler(filters.Sticker.ALL, send_sticker)
    voice_handler = MessageHandler(filters.VOICE, send_voice)
    # application.add_handler(get_message)


    application.add_handler(start_handler)
    # запускаем приложение
    application.run_polling()
