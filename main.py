from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ChatType
import json
from config import *

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class addKeyWord(StatesGroup):
    keyWord = State()


class removeKeyWord(StatesGroup):
    keyWord = State()


class addMyChat(StatesGroup):
    chat = State()


class removeMyChat(StatesGroup):
    chat = State()


class addAdmin(StatesGroup):
    admin = State()


class removeAdmin(StatesGroup):
    admin = State()


def listOfKeyWords():
    with open('db.json', 'r', encoding='utf-8') as file:
        return json.load(file)['keyWords']


def listOfAll():
    with open('db.json', 'r', encoding='utf-8') as file:
        return json.load(file)


def listOfMyChats():
    with open('db.json', 'r', encoding='utf-8') as file:
        return json.load(file)['myChats']


def listOfMyChatsId():
    with open('db.json', 'r', encoding='utf-8') as file:
        myChats = json.load(file)['myChats']
        returnList = []
        for chat in myChats:
            returnList.append(chat['id'])
        return returnList


def listOfMyChatsTitle():
    with open('db.json', 'r', encoding='utf-8') as file:
        myChats = json.load(file)['myChats']
        returnList = []
        for chat in myChats:
            returnList.append(chat['title'])
        return returnList


def listOfBotAdminsId():
    with open('db.json', 'r', encoding='utf-8') as file:
        botAdmins = json.load(file)['botAdmins']
        returnList = []
        for admin in botAdmins:
            returnList.append(admin['id'])
        return returnList


def listOfBotAdminsName():
    with open('db.json', 'r', encoding='utf-8') as file:
        botAdmins = json.load(file)['botAdmins']
        returnList = []
        for admin in botAdmins:
            returnList.append(admin['name'])
        return returnList


@dp.message_handler(commands=['start'], chat_type=types.ChatType.PRIVATE)
async def process_start_command(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        keyboard_markup.row(types.KeyboardButton('Мои ключевые слова'))
        keyboard_markup.row(types.KeyboardButton('Добавить ключевое слово'),
                            types.KeyboardButton('Удалить ключевое слово'))
        keyboard_markup.row(types.KeyboardButton('Мои чаты'))
        keyboard_markup.row(types.KeyboardButton('Добавить чат'),
                            types.KeyboardButton('Удалить чат'))
        keyboard_markup.row(types.KeyboardButton('Мои админы'))
        keyboard_markup.row(types.KeyboardButton('Добавить админа'),
                            types.KeyboardButton('Убрать админа'))

        await bot.send_message(message.from_user.id, 'Привет, админ', reply_markup=keyboard_markup)


@dp.message_handler(chat_type=[types.ChatType.GROUP, types.ChatType.SUPERGROUP])
async def echo_message(message: types.Message):
    if message.text in listOfKeyWords() and message.chat.id in listOfMyChatsId():
        for i in listOfBotAdminsId():
            await bot.send_message(i, f'В чате {message.chat.title} '
                                      f'пользователь {message.from_user.first_name} написал: "{message.text}"\n'
                                      f'{message.link("Ссылка на сообщение")}', parse_mode='HTML')


@dp.message_handler(text='Мои ключевые слова', chat_type=types.ChatType.PRIVATE)
async def myKeyWordsMsg(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        if len(listOfKeyWords()) > 1:
            await bot.send_message(message.from_user.id, f'<b>Список ваших ключевых слов:</b>\n'
                                                         f'{", ".join(listOfKeyWords())}', parse_mode='HTML')
        else:
            await bot.send_message(message.from_user.id, f'<b>Ваше ключевое слово:</b>\n'
                                                         f'{listOfKeyWords()[0]}', parse_mode='HTML')


@dp.message_handler(text='Мои чаты', chat_type=types.ChatType.PRIVATE)
async def myChats(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        if len(listOfMyChatsTitle()) > 1:
            await bot.send_message(message.from_user.id, f'<b>Список ваших чатов:</b>\n'
                                                         f'{", ".join(listOfMyChatsTitle())}', parse_mode='HTML')
        else:
            await bot.send_message(message.from_user.id, f'<b>Ваш чат:</b>\n'
                                                         f'{listOfMyChatsTitle()[0]}', parse_mode='HTML')


@dp.message_handler(text='Мои админы', chat_type=types.ChatType.PRIVATE)
async def myAdmins(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        if len(listOfBotAdminsId()) > 1:
            await bot.send_message(message.from_user.id, f'<b>Список ваших админов:</b>\n'
                                                         f'{", ".join(listOfBotAdminsName())}', parse_mode='HTML')
        else:
            await bot.send_message(message.from_user.id, f'<b>Админ:</b>\n'
                                                         f'{listOfBotAdminsName()[0]}', parse_mode='HTML')


@dp.message_handler(text='Добавить ключевое слово', chat_type=types.ChatType.PRIVATE)
async def addKeyWordsMsg(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        await addKeyWord.keyWord.set()
        await bot.send_message(message.from_user.id, 'Введите слово, которое вы хотите добавить в список:')


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=addKeyWord.keyWord)
async def addKeyWordsEnd(message: types.Message, state):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        newFile = listOfAll()
        newFile['keyWords'].append(message.text)

        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(newFile, file)

        await bot.send_message(message.from_user.id, f'Я только что добавил слово "{message.text}"')
        await state.finish()


@dp.message_handler(text='Удалить ключевое слово', chat_type=types.ChatType.PRIVATE)
async def removeKeyWordsMsg(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        await removeKeyWord.keyWord.set()
        await bot.send_message(message.from_user.id, 'Введите слово, которое вы хотите удалить из списка:')


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=removeKeyWord.keyWord)
async def removeKeyWordsEnd(message: types.Message, state):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        newFile = listOfAll()
        try:
            del newFile['keyWords'][newFile['keyWords'].index(message.text)]
        except ValueError:
            await bot.send_message(message.from_user.id, f'Такого слова в списке нет')
            await state.finish()
            return 0

        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(newFile, file)

        await bot.send_message(message.from_user.id, f'Я только что удалил слово "{message.text}"')
        await state.finish()


@dp.message_handler(text='Добавить чат', chat_type=types.ChatType.PRIVATE)
async def addChat(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        await addMyChat.chat.set()
        await bot.send_message(message.from_user.id, 'Введите ID чата, который вы хотите добавить:')


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=addMyChat.chat)
async def addChatEnd(message: types.Message, state):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        newFile = listOfAll()
        try:
            chat = await bot.get_chat(int(message.text))
        except Exception:
            await bot.send_message(message.from_user.id, f'Такого чата не существует')
            await state.finish()
            return 0

        if chat.title is not None:
            newFile['myChats'].append({"id": int(message.text), "title": chat.title})
        else:
            newFile['myChats'].append({"id": int(message.text), "title": chat.first_name})

        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(newFile, file)

        await bot.send_message(message.from_user.id, f'Я только что добавил чат "{chat.title}"')
        await state.finish()


@dp.message_handler(text='Удалить чат', chat_type=types.ChatType.PRIVATE)
async def removeMyChatsMsg(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        await removeMyChat.chat.set()
        await bot.send_message(message.from_user.id, 'Введите ID чата, который вы хотите удалить:')


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=removeMyChat.chat)
async def removeMyChatsEnd(message: types.Message, state):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        newFile = listOfAll()
        try:
            for i in newFile['myChats']:
                if i['id'] == int(message.text):
                    chat_name = newFile['myChats'][newFile['myChats'].index(i)]['title']
                    del newFile['myChats'][newFile['myChats'].index(i)]
        except Exception:
            await bot.send_message(message.from_user.id, f'Такого чата в списке нет')
            await state.finish()
            return 0

        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(newFile, file)

        await bot.send_message(message.from_user.id, f'Я только что удалил чат "{chat_name}"')
        await state.finish()


@dp.message_handler(text='Добавить админа', chat_type=types.ChatType.PRIVATE)
async def addMyAdmin(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        await addAdmin.admin.set()
        await bot.send_message(message.from_user.id, 'Введите ID админа, которого вы хотите добавить:')


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=addAdmin.admin)
async def addMyAdminEnd(message: types.Message, state):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        newFile = listOfAll()
        msg = await bot.send_message(int(message.text), 'test')
        adminName = msg['chat']['first_name']

        newFile['botAdmins'].append({"id": int(message.text), "name": adminName})

        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(newFile, file)

        await bot.send_message(message.from_user.id, f'Я только что добавил админа "{adminName}"')
        await state.finish()


@dp.message_handler(text='Убрать админа', chat_type=types.ChatType.PRIVATE)
async def removeMyAdmin(message: types.Message):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        await removeAdmin.admin.set()
        await bot.send_message(message.from_user.id, 'Введите ID админа, которого вы хотите удалить:')


@dp.message_handler(chat_type=types.ChatType.PRIVATE, state=removeAdmin.admin)
async def removeMyAdminEnd(message: types.Message, state):
    if message.from_user.id not in listOfBotAdminsId():
        await bot.send_message(message.from_user.id, 'Извините, но вы не можете пользоваться ботом')
    else:
        newFile = listOfAll()
        try:
            for i in newFile['botAdmins']:
                if i['id'] == int(message.text):
                    admin_name = newFile['botAdmins'][newFile['botAdmins'].index(i)]['name']
                    del newFile['botAdmins'][newFile['botAdmins'].index(i)]
        except ValueError:
            await bot.send_message(message.from_user.id, f'Такого админа в списке нет')
            await state.finish()
            return 0

        with open('db.json', 'w', encoding='utf-8') as file:
            json.dump(newFile, file)

        await bot.send_message(message.from_user.id, f'Я только что удалил админа "{admin_name}"')
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp)
