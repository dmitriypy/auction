from aiogram.dispatcher import FSMContext
from aiogram import types

from data.xjetapi import api
import db

ADMINS = [5802478361]


async def start_auction(message: types.Message, state: FSMContext):
    if message.from_user.id in ADMINS:
        await message.answer("Привет! Введи айди аукциона: ")

        await state.set_state("start_next_step")

async def got_uid(message: types.Message, state: FSMContext):
    try:
        msg = float(message.text)
    except:
        msg = "pon"

    if isinstance(msg, int):
        if db.check_auction(message.text):
            await message.answer("Аукцион с данным айди уже существует!!!")
            await state.finish()
            return

        db.add_auction(message.text)
        await state.update_data(uid=message.text)

        await message.answer("Готово! Введите начальную ставку аукциона: ")
        
        await state.set_state("got_start_bid")

    else:
        await message.reply("Не правильный айди аукциона! Попробуй ещё раз: /auction")
        await state.finish()

async def got_start_bid(message: types.Message, state: FSMContext):
    try:
        message.text = float(message.text)
    except:
        pass

    if isinstance(message.text, float) or isinstance(message.text, int):
        user_data = await state.get_data()

        db.add_balance(user_data["uid"], message.text)
        
        await message.answer(f"Готово! Ссылка аукциона: https://t.me/username?start={user_data['uid']}")
        await state.finish()


    else:
        await message.reply("Не правильная сумма! Попробуй ещё раз: /auction")
        await state.finish()
