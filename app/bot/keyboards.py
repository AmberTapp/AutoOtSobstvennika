
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = [
        [InlineKeyboardButton(text="Я продавец", callback_data="seller")],
        [InlineKeyboardButton(text="Я покупатель", callback_data="buyer")],
        [InlineKeyboardButton(text="Последние авто", callback_data="feed")],
        [InlineKeyboardButton(text="Премиум / бусты", callback_data="billing")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def billing_kb(link_basic: str, link_pro: str, link_boost: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Basic — оплатить (TON)", url=link_basic)],
        [InlineKeyboardButton(text="Pro — оплатить (TON)", url=link_pro)],
        [InlineKeyboardButton(text="Boost объявления — оплатить (TON)", url=link_boost)],
    ])
