import telegram
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder
import asyncio
import random

# Список пользователей, которым разрешено общаться между собой
# Можно добавить свои айди пользователей, разделив их запятой

# Словарь для хранения активных чатов между пользователями
active_chats = {}
free_id = []


async def start(update, context):
    """Отправляет приветственное сообщение при запуске бота"""
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Привет! Я бот для обмена сообщениями. '
                                        'Напишите /connect для начала общения.')


async def connect(update, context):
    if free_id == [] or free_id[0]==update.effective_user.id:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Ожидайте, пока мы найдём собеседника')
        user_id = update.effective_user.id
        free_id.append(user_id)
        print(free_id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='*Собеседник найден, напишите сообщение*'
                                            'Введите /disconnect для поиска другого человека')

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

async def disconnect(update, context):
    if free_id == []:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='Вы вышли из диалога, ожидайте, пока мы найдём нового собеседника.'
                                            'Используйте /exit, если не хотите искать собеседника')
        user_id = update.effective_user.id
        user2_id = active_chats[user_id]
        free_id.append(user2_id)
        await context.bot.send_message(chat_id=user2_id,
                                       text='Собеседник вышел из диалога, ожидайте, пока мы найдём нового собеседника.'
                                            'Используйте /exit, если не хотите искать собеседника')
        print(free_id)
        if user_id in active_chats:
            active_chats.pop(user_id)
        else:
            user2_id = get_key(user_id)
            active_chats.pop(user2_id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='*Собеседник найден, напишите сообщение*')

        user_id = update.effective_user.id
        print(free_id)
        id = random.randint(0, len(free_id)-1)
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
    connect_handler = CommandHandler('connect', connect)
    disconnect_handler = CommandHandler('disconnect', disconnect)
    # регистрируем обработчик в приложение
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
