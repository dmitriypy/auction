from aiogram import Dispatcher

from handlers.text.start import bot_start, check_payments
from handlers.text.auction import start_auction, got_uid, got_start_bid

def register_user_handler(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=['start'], state='*')
    dp.register_callback_query_handler(check_payments, state='invoice')

    dp.register_message_handler(start_auction, commands=['auction'], state='*')
    dp.register_message_handler(got_uid, state='start_next_step')
    dp.register_message_handler(got_start_bid, state='got_start_bid')