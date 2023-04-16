from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import db
from data.xjetapi import api


def extract_unique_code(text, ):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

async def bot_start(message: types.Message, state: FSMContext):
    unique_code = extract_unique_code(message.text)
    if unique_code:
        if not db.check_auction(unique_code):
            await state.finish()
            return
        
        await state.update_data(uid=unique_code)

        #если есть id рефера
        auction_amount = db.get_balance(unique_code)


        try:
            invoice = await api.invoice_create(currency="ton", amount=auction_amount)
            print(invoice)
            print(invoice["external_link"])
        except Exception as e:
            await message.reply(e)
            await state.finish()
            return

        invoice_button = InlineKeyboardButton('Оплатить счёт',
                                              url=invoice['external_link'])

        check_payment = InlineKeyboardButton(text='Проверить оплату',
                                             callback_data=f"invoice_{invoice['invoice_id']}")

        cancel_payment = InlineKeyboardButton(text='◀️ Назад', 
                                              callback_data="pon")
#◀️
        start_keyboard = InlineKeyboardMarkup(row_width=1)
        
        start_keyboard.add(invoice_button, check_payment, cancel_payment)

        await message.answer(f"Оплатите данный счёт на сумму в {auction_amount} TON чтобы поставить ставку!", reply_markup=start_keyboard)


        await state.set_state("invoice")

    else:
        #если в ссылке нет id рефера
        await message.reply("id is NaN!")

async def check_payments(call: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    callback_data = call["data"]
    print(call)

    if "pon" in callback_data:
        await call.message.delete()
        await state.finish()
        return


    if "invoice_" in callback_data:
        
        payment_status = await api.invoice_status(callback_data.replace("invoice_", ""))
        
        if payment_status["payments"] != []:
            now_balance = db.get_balance(user_data["uid"])
            db.add_balance(user_data["uid"], (now_balance/100)*5)

            await call.bot.send_message(call.message.chat.id, text=f"Успех! Вы успешно поставили ставку!")
            
            await call.message.delete()
            await state.finish()
            return
        
        else:
            await call.answer("Счёт не оплачен!")
        
    await state.set_state("invoice")