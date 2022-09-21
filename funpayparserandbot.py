import requests
from bs4 import BeautifulSoup as b
from aiogram import types, executor, Dispatcher, Bot
URL = 'https://funpay.com/lots/700/'
TOKEN = 'your token'

r = requests.get(URL)
soup = b(r.text, 'html.parser')
lotnames = soup.find_all('div', class_='tc-desc-text')
sellers = soup.find_all('div', class_='media-user-name')
mass_of_lotnames = [i.text for i in lotnames]
mass_of_sellers = [el.text for el in sellers]
reviews = soup.find_all('div', class_='media-user-reviews')
mass_of_reviews = [c.text for c in reviews]
prices = soup.find_all('div', class_='tc-price')
mass_of_prices = [j.text for j in prices]
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def begin(message: types.Message):
    await bot.send_message(message.chat.id, """
Напиши "/all" если хочешь чтобы бот отправил тебе первые 10 объявлений на данную категорию
Напиши "/amount" если хочешь чтобы бот отправил тебе количество объявлений на данный момент по этой категории
Напиши цифру и ты увидешь конкретный елемент по этой цифре
""")

@dp.message_handler(content_types=['text'])
async def all(message: types.Message):
    if message.text.lower() == '/all':
        await bot.send_message(message.chat.id, (',').join(mass_of_lotnames[0:10]))
    elif message.text.lower() == '/amount':
        await bot.send_message(message.chat.id, len(mass_of_lotnames))
    elif message.text in '0123456789':
        await bot.send_message(message.chat.id, f'ТОВАР: {mass_of_lotnames[int(message.text)-1]}')
        await bot.send_message(message.chat.id, f'ПРОДАВЕЦ:{mass_of_sellers[int(message.text)-1]}')
        await bot.send_message(message.chat.id, f'ОТЗЫВЫ: {mass_of_reviews[int(message.text)-1]}')
        await bot.send_message(message.chat.id, f'ЦЕНА: {mass_of_prices[int(message.text)-1]}')
        print(mass_of_reviews[int(message.text)])
executor.start_polling(dp)