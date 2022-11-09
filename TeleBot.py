from config import token  #импортируем token
import telebot
from telebot import types

token = token
bot = telebot.TeleBot(token)  # запускаем бота

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # создаем кнопки, и количество рядов
btn_address = types.KeyboardButton('Адреса магазинов')
pan_katalog = types.KeyboardButton('Каталог товаров')
btn_payment = types.KeyboardButton('Способы оплаты')
btn_dilivery = types.KeyboardButton('Способы доставки')
zamer = types.KeyboardButton('Заказать замер')
send_m = types.KeyboardButton('Связь со специалистом')
sale = types.KeyboardButton('Акции')
markup_menu.add(btn_address, btn_payment, btn_dilivery, pan_katalog, sale, zamer, send_m)

markup_inline_payment = types.InlineKeyboardMarkup()  # создаем вложенные кнопки
btn_cash = types.InlineKeyboardButton('Наличные', callback_data='cash')
btn_bank = types.InlineKeyboardButton('Кредит', callback_data='bank')
btn_otsr = types.InlineKeyboardButton('Отсрочка', callback_data='otsr')
markup_inline_payment.add(btn_cash, btn_bank, btn_otsr)

markup_inline_katalog = types.InlineKeyboardMarkup()  # создаем вложенные кнопки
btn_saiding = types.InlineKeyboardButton('Сайдинг', url='      ', callback_data='said')
btn_dpk = types.InlineKeyboardButton('Террасная доска', url='      ',
                                     callback_data='dpk')
btn_vodostok = types.InlineKeyboardButton('Водосточные системы',
                                          url='         ',
                                          callback_data='vodost')
markup_inline_katalog.add(btn_saiding, btn_dpk, btn_vodostok)


@bot.message_handler(commands=['start', 'help'])  # отправка приветственного сообщения
def send_welcome(message):
    mention = f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>'
    bot.send_message(message.chat.id, f"Здравствуйте, {mention}! \nЯ бот компании __________", parse_mode="HTML")


@bot.message_handler(func=lambda message: True)  # действия при нажатии на кнопки
def echo_all(message):
    if message.text == 'Способы доставки':
        bot.reply_to(message, "Наша компания осуществляет доставку по всей республике в том числе бесплатную"
                              " (подробнее смотрите в разделе 'Акции'", reply_markup=markup_menu)
    elif message.text == 'Способы оплаты':
        bot.reply_to(message, "Способы оплаты", reply_markup=markup_inline_payment)
    elif message.text == 'Акции':
        bot.reply_to(message, '''можно размещать наши акции ''', reply_markup=markup_menu)

    elif message.text == 'Каталог товаров':
        bot.reply_to(message, "Много всeго полезного ", reply_markup=markup_inline_katalog)

    elif message.text == 'Адреса магазинов':
        bot.reply_to(message, "Розничный магазин \nТД 'Ждановичи', г. Минск, \nул. Тимирязьева 125, к4, \n"
                              "\nРозничный магазин \nТД 'ЛенинГрад' , г. Минск, \nул. Ленина 27",
                     reply_markup=markup_menu)
    elif message.text == 'Заказать замер':
        bot.reply_to(message, "Здесь можно перенапривить клиента специалисту или добавить заявку в Битрикс",
                     reply_markup=markup_menu)
    else:
        bot.reply_to(message, message.text, reply_markup=markup_menu)


# действия при при нажатии на вложенные кнопки
@bot.callback_query_handler(func=lambda call: call.data in ('cash', 'bank', 'otsr'))
def call_back_payment(call):
    if call.data == 'cash':
        bot.send_message(call.message.chat.id, text='''Вы можете приобрести товар за наличные и по карте в наших
         фирменных магазинах  
        ''', reply_markup=markup_inline_payment)
    elif call.data == 'bank':
        bot.send_message(call.message.chat.id, text='''Специалисты нашей компании помогут оформить кредит в наших 
        банках - партнерах
        ''', reply_markup=markup_inline_payment)
    elif call.data == 'otsr':
        bot.send_message(call.message.chat.id, text='''Товар можно приобрести по внутренней отсрочке на один 
        охулиард лет
        ''', reply_markup=markup_inline_payment)


@bot.callback_query_handler(func=lambda tell: tell.data in ('said', 'dpk', 'vodost'))
def call_back_katalog(tell):  # действия при нажатии на вложенные кнопки каталог
    if tell.data == 'said':
        bot.send_message(tell.message.chat.id, text='',
                         reply_markup=markup_inline_katalog)
    elif tell.data == 'dpk':
        bot.send_message(tell.message.chat.id, text='',
                         reply_markup=markup_inline_katalog)
    elif tell.data == 'vodost':
        bot.send_message(tell.message.chat.id, text='',
                         reply_markup=markup_inline_katalog)


bot.polling(none_stop=True, interval=0)  # зацикливаем работу

