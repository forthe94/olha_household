import asyncio
import dataclasses
import time
import datetime
import json
import os
from collections import defaultdict

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from google_sheets import get_sheets, get_items, add_item_to_sheet
from subs_secrets import substitude_serv_acc

BOT_TOKEN = os.getenv('BOT_API_TOKEN')
PORT = int(os.environ.get('PORT', 80))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

googlesheet_id = '1fika6X6aCOBhUV882FoS897QrXmtSkxOdCQvrEXYitI'

stages = defaultdict(int)
names = [['Саша', 'Женя', 'Крутов', 'Ангелина', 'Катя', 'Отмена']]
chosen_name = {}
chosen_sheet = {}


async def name_choose_stage():
    name_choose_kb = ReplyKeyboardMarkup(names, resize_keyboard=True)

    return name_choose_kb


async def sheet_choose_stage():
    sheets = get_sheets(googlesheet_id)
    sheet_choose_kb = ReplyKeyboardMarkup([[sheet.title for sheet in sheets] + ['Отмена']], resize_keyboard=True)
    return sheet_choose_kb


async def item_choose_stage(sheet: str):
    items = get_items(googlesheet_id, sheet)

    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items + ['Отмена']:
        kb.add(KeyboardButton(item))
    return kb


@dp.message_handler()
async def default_message(message: types.Message):
    reply_keyboard = None
    if message.text == 'Отмена':
        stages[message.chat.id] = 0

    stage = stages[message.chat.id]
    try:
        if stage == 1:
            chosen_name[message.chat.id] = message.text
            answer = 'Выбери страницу'
            reply_keyboard = await sheet_choose_stage()
            stages[message.chat.id] = 2
        elif stage == 2:
            chosen_sheet[message.chat.id] = message.text
            reply_keyboard = await item_choose_stage(message.text)
            answer = 'Выбери дело/расход'
            stages[message.chat.id] = 3
        elif stage == 3:
            item = message.text
            name = chosen_name[message.chat.id]
            sheet = chosen_sheet[message.chat.id]
            add_item_to_sheet(googlesheet_id, name, sheet, item)
            answer = 'Готово! Добавить еще дело/расход? Выбирай кому'
            reply_keyboard = await name_choose_stage()
            stages[message.chat.id] = 1

        else:
            reply_keyboard = await name_choose_stage()
            answer = 'Выбери кому добавить дело/расход'
            stages[message.chat.id] = 1

        await message.answer(answer, reply_markup=reply_keyboard)
    except:
        await message.answer('ты что-то поломал возвращаемся обратно', reply_markup=reply_keyboard)
        stages[message.chat.id] = 0

async def on_startup(dp):
    await bot.set_webhook('https://olha-household.herokuapp.com/')

if __name__ == '__main__':
    print('Bot started')
    substitude_serv_acc()

    loop = asyncio.get_event_loop()
    # executor.start_polling(dispatcher=dp, loop=loop)

    executor.start_webhook(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        webhook_path='',
        port=PORT,
        host='0.0.0.0'
    )
