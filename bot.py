import config
import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from random import randint
import sqlite3 

bot = telebot.TeleBot(config.API_TOKEN)

def senf_info(bot, message, row):
        
        info = f"""
📍Title of movie:   {row[2]}
📍Year:                   {row[3]}
📍Genres:              {row[4]}
📍Rating IMDB:      {row[5]}


🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻
{row[6]}
"""
        bot.send_photo(message.chat.id,row[1])
        bot.send_message(message.chat.id, info)


def main_markup():
  markup = ReplyKeyboardMarkup()
  markup.add(KeyboardButton('/random'))
  return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Hello! You're welcome to the best Movie-Chat-Bot🎥!
Here you can find 1000 movies 🔥
Click /random to get random movie
Or write the title of movie and I will try to find it! 🎬 """, reply_markup=main_markup())


@bot.message_handler(commands=['random'])
def random_movie(message):
    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM movies ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)


@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, """ Я тебе помогу!!!
                     /help
/genre - после чего тебе нужно написать жанр на английском, с большой буквы, после чего тебе выдатут фильм с этим жанром
                     
/year - чабарнутая штука, которая выдаёт тебе фильм по дате выпуска (нужно писать так: пишем мначала знак >, < или = затем в '' пишем: год)
                     
/rating - сортирует по рейтингу, пишем почти также, как и /year (знак >, < или =, затем в '' пишем: цифра.цифра)
                     
/random - выдаёт тебе рандомный фильм
                     
если подумали: а где же избранное? То обломитесь, если понравилось, сразу смотрите
            
                ВСЁ!""", reply_markup=main_markup())


@bot.message_handler(content_types=['text'])
def hello(message):
    if message.text == '/genre':
        sent = bot.send_message(message.from_user.id, "Введите жанр с большой буквы и на инглиш")
        bot.register_next_step_handler(sent, genress)
    elif message.text == '/year':
        sent2 = bot.send_message(message.from_user.id, "Введите чабарнутость")
        bot.register_next_step_handler(sent2, yearss)
    else:
        if message.text == '/rating':
            sent3 = bot.send_message(message.from_user.id, "Введите чабарнутость номер 2")
            bot.register_next_step_handler(sent3, ratingg)


def genress(message): 
    genres = message.text
    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM movies WHERE genre LIKE '%{genres}%' ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)


def yearss(message): 
    sent2 = message.text
    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM movies WHERE year {sent2} ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)


def ratingg(message):
    sent3 = message.text
    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM movies WHERE rating {sent3} ORDER BY RANDOM() LIMIT 1")
        row = cur.fetchall()[0]
        cur.close()
    senf_info(bot, message, row)

    
@bot.message_handler(func=lambda message: True)
def echo_message(message):

    con = sqlite3.connect("movie_database.db")
    with con:
        cur = con.cursor()
        cur.execute(f"select * from movies where LOWER(title) = '{message.text.lower()}'")
        row = cur.fetchall()
        if row:
            row = row[0]
            bot.send_message(message.chat.id,"Of course! I know this movie😌")
            senf_info(bot, message, row)
        else:
            bot.send_message(message.chat.id,"I don't know this movie ")

        cur.close()



bot.infinity_polling()
