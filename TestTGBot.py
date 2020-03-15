import config
import telebot
import psycopg2
from random import choice

conn = psycopg2.connect(dbname = config.dbname, user = config.dbuser, 
                        password = config.dbpassword, host = config.dbhost)
cursor = conn.cursor()

ok_list = ['Ага, записал. Продолжай.',
           'Хорошо.',
           'Ты точно уверен?',
           'Ну, допустим',
           'Так и запишем, значит. Отличненько.',
           'Буду иметь в виду.']

bot = telebot.TeleBot(config.token)
#keyboard1 = telebot.types.ReplyKeyboardMarkup()
#keyboard1.row('Случайная моя реплика', 'Случайная реплика')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Я, короче, бот для теситрования базы данных. Ты мне чего-нибудь пишешь, а я это записываю в базу данных и храню. Правда занимательно? Я обещаю ничего из того, что ты мне скажешь, против тебя не использовать. Честно-честно ) Можешь дать волю фантазии.')
    bot.send_message(message.chat.id, 'А еще я могу разболтать тебе то, что у меня в базе данных записано. Напиши /random и я пришлю тебе случайное сообщение из тех, что записаны у меня в базе. Но будь остарожен - люди мне всякое пишут.')

@bot.message_handler(commands=['random'])
def random_message(message):
    cursor.execute('select c.message_text from public.chats c order by random() limit 1')
    random_message_text, = cursor.fetchone()
    bot.send_message(message.chat.id, random_message_text)


@bot.message_handler(content_types=['text'])
def send_text(message):
    message_text = message.text
    chat_id = message.chat.id
    date_unix = message.date
    message_text_lower = message_text.lower()

    cursor.execute("""insert into public.chats (message_text, chat_id, date_unix) 
                    values (%(message_text)s, %(chat_id)s, %(date_unix)s)""", {
                       'message_text' : message_text,
                       'chat_id' : chat_id,
                       'date_unix' : date_unix
                       })

    conn.commit()

    bot.send_message(message.chat.id, choice(ok_list))

    #if message_text_lower == 'привет':
    #    bot.send_message(message.chat.id, 'Типа того, да. И тебе привет.')
    #elif message_text_lower == 'пока':
    #    bot.send_message(message.chat.id, 'Ну, бывай')
    #elif message_text_lower == 'отправь мне стикер':
    #    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIIp15eT-L59ul7L3FB2DQ5qZJwq7yPAAKoAANgD00MiDLCkdBP8mkYBA')

@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    print(message)

bot.polling()
