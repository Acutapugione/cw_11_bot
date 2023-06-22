import logging
from aiogram import Bot, Dispatcher, executor, types
import random
import json
from aiogram.types import InlineKeyboardButton as in_kb 
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=json.load(open("secrets.json")).get("API_TOKEN"))
dp = Dispatcher(bot)
is_echo = False


@dp.message_handler(commands=["start"])
async def welcome(message):
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🎲 Рандомне число", callback_data="random"),
            ],
            [
                types.InlineKeyboardButton("😊 Як справи?", callback_data="howdy"),
                types.InlineKeyboardButton("Ехо бот", callback_data="echo"),
            ],
            [
                types.InlineKeyboardButton("Фільми", callback_data="films")
            ]
        ]
    )
    bot_data = await bot.get_me()
    text = f"""Привіт,{bot_data.first_name}!
    Я - <b>{message.from_user.first_name}</b>
    , бот створний для тесту."""
    await bot.send_message(
        message.chat.id, text, parse_mode="html", reply_markup=markup
    )


@dp.callback_query_handler(lambda callb: callb.data == "random")
async def execute_random(callb: types.CallbackQuery):
    await callb.answer(str(random.randint(0, 100)))


@dp.callback_query_handler(lambda callb: callb.data == "howdy")
async def execute_howdy(callb: types.CallbackQuery):
    markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
            [
                types.InlineKeyboardButton("Добре", callback_data="good"),
                types.InlineKeyboardButton("Не дуже", callback_data="bad"),
            ]
        ],
    )
    await callb.message.answer("Супер а сам як", reply_markup=markup)


@dp.callback_query_handler(lambda callb: callb.data == "echo")
async def execute_echo(callb: types.CallbackQuery):
    global is_echo
    is_echo = not is_echo
    await callb.answer('Echo '+ 'On' if is_echo else 'Off')


@dp.message_handler(content_types=["text"])
async def lalala(message: types.Message):
    if is_echo:
        await message.answer(message.text)

@dp.callback_query_handler(lambda callb: callb.data == 'films')
async def get_films(callb:types.CallbackQuery):
    films = json.load(open("data/films.json")).get("films")

    buttons = [ in_kb(x.get('name'), callback_data= f'film/{films.index(x)}') for x in films ]
    markup = types.InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=[
        buttons[:len(buttons)//2],
        buttons[len(buttons)//2:]
        ],
    )
    await callb.message.answer('Виберіть фільм', reply_markup=markup)

@dp.callback_query_handler(lambda callb: str(callb.data).startswith('film/')) 
async def get_film_info(callb:types.CallbackQuery):
    films = json.load(open("data/films.json")).get("films")
    film_id = int(callb.data.split('/')[-1])
    await callb.message.reply(films[film_id])
    
    
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
