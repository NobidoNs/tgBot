import telebot
import time
from telebot import types
from datetime import datetime

class sqll():

  def __init__(self):
    self.cur = None


class money():

  def __init__(self):
    self.money = None


def clickerConnectSteps(message, lastStep, nextStep=None):
  if lastStep == 0:
    CCinitMsg(message, 'initMsg')
  elif lastStep == 'initMsg':
    CCmenu(message)
    #
  elif lastStep == 'menu':
    if nextStep == 'testAC':
      CCinstruction(message, 'testAC')
    elif nextStep == 'timeCon':
      CCdayscount(message, 'daysCount')
    elif nextStep == 'bayUnlim':
      CCpay(message, 'bayUnlim', True)
    #
  elif lastStep == 'testAC':
    if message.text == 'Обратиться в поддержку':
      support(message)
    elif message.text == 'Готов отправить':
      CCsend(message, '1')
    #
  elif message.text == 'timeCon':
    CCdayscount(message, 'daysCount')
  elif lastStep == 'daysCount':
    CCpay(message, 'pay')
  elif lastStep == 'pay':
    if message.text == 'Оплатил':
      CCinstruction(message, 'timeSend')
    else:
      support(message)
  elif lastStep == 'timeSend':
    CCsend(message, Money.money // priceDay)
    #
  elif lastStep == 'bayUnlim':
    if message.text == 'Обратиться в поддержку':
      support(message)
    else:
      bayUnlim(message)


def bayUnlim(message):
  firstname = message.from_user.first_name
  username = message.from_user.username
  bot.send_message(
      chatID,
      "('%s', '%s', '%s', '%s', '%s')" % (time.time(), str(
          datetime.now()), firstname, username, 'BAY UNLIMITED PROGRAM'))
  bot.send_message(message.chat.id,
                   "Ожидайте, с вами свяжутся или обратитесь в поддержку")
  menu(message)


def CCpay(message, stepName, unlim=False):
  if unlim == True:
    Money.money =  priceUnlim
  else:
    try:
      days = int(message.text)
    except:
      bot.send_message(message.chat.id,
                       "Вы ввели не коректное число, попробуйте снова")
      CCdayscount(message, 'daysCount')
    Money.money = days * priceDay
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  btn1 = types.KeyboardButton("Оплатил")
  btn2 = types.KeyboardButton("Обратиться в поддержку")
  markup.row(btn1)
  markup.row(btn2)
  bot.send_message(message.chat.id,
                   "Оплатите %s рублей по номеру карты: 9999999999999999" %
                   Money.money,
                   reply_markup=markup)
  bot.register_next_step_handler(message, clickerConnectSteps, stepName)


def CCdayscount(message, stepName):
  bot.send_message(message.chat.id, "На сколько дней?")
  bot.register_next_step_handler(message, clickerConnectSteps, stepName)


def support(message):
  bot.send_message(message.chat.id, "Опишите проблему")
  bot.register_next_step_handler(message, supp)


def supp(message):
  msg = message.text.strip()
  firstname = message.from_user.first_name
  username = message.from_user.username

  bot.send_message(
      chatID, "SUPPORT: ('%s', '%s', '%s', '%s', '%s')" %
      (time.time(), str(datetime.now()), firstname, username, msg))
  bot.send_message(message.chat.id, "Ваше обращение отправленно")
  menu(message)


def CCsend(message, dur):
  bot.send_message(message.chat.id, "Вставьте текст")
  bot.register_next_step_handler(message, CCaddTokenToBD, dur)


def CCaddTokenToBD(message, duration):
  token = message.text.strip()
  msg = token + str(duration)
  firstname = message.from_user.first_name
  username = message.from_user.username
  bot.send_message(
      chatID,
      f'Add Token: {time.time()}, {str(datetime.now())}, {firstname}, {username}, {msg}'
  )
  bot.send_message(
      message.chat.id,
      "Всё готово, кликер перезапускается ежедневно в N по МСК")
  menu(message)


def CCinstruction(message, stepName):
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  btn1 = types.KeyboardButton("Готов отправить")
  btn2 = types.KeyboardButton("Обратиться в поддержку")
  markup.row(btn1)
  markup.row(btn2)
  msg = 'test'
  bot.send_message(message.chat.id, msg, reply_markup=markup)
  bot.register_next_step_handler(message, clickerConnectSteps, stepName)


def CCmenu(message):
  markup = types.InlineKeyboardMarkup()
  testAC = types.InlineKeyboardButton('Протестировать (1 час)',
                                      callback_data='testAC')
  timeCon = types.InlineKeyboardButton('Подключить на время',
                                       callback_data='timeCon')
  bayUnlim = types.InlineKeyboardButton('Купить навсегда',
                                        callback_data='bayUnlim')
  back = types.InlineKeyboardButton('Назад', callback_data='back')

  markup.row(testAC)
  markup.row(timeCon)
  markup.row(bayUnlim)
  markup.row(back)

  bot.send_message(message.chat.id, 'service', reply_markup=markup)


def CCinitMsg(message, stepName):
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  btn1 = types.KeyboardButton("Продолжить")
  markup.row(btn1)
  msg = 'price and conditions'
  bot.send_message(message.chat.id, msg, reply_markup=markup)
  bot.register_next_step_handler(message, clickerConnectSteps, stepName)


def outI(message):
  msg = 'info'
  bot.send_message(message.chat.id, msg)
  menuBtn(message)


def howMany(message):
  msg = 'info'
  bot.send_message(message.chat.id, msg)
  menuBtn(message)


def upgrageSteps(message, curStep):
  nextStep = curStep + 1
  msgs = [
      'msg1',
      'msg2',
      'msg3',
      'msg4'
  ]
  photos = [
      'url', 'url',
      'url', None
  ]

  if curStep < 3:
    upgradeStep(message, nextStep, msgs[curStep], photos[curStep])
  elif curStep == 3:
    upgradeStep(message, nextStep, msgs[curStep], photos[curStep], True)

  elif curStep == 4:
    menu(message)


def upgradeStep(message, nextStep, msg, photo, last=False):
  if last == True:
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  else:
    markup = types.ReplyKeyboardMarkup()
  btnNext = types.KeyboardButton("Продолжить")
  markup.row(btnNext)
  if photo != None:
    bot.send_photo(message.chat.id, photo)

  bot.send_message(message.chat.id, msg, reply_markup=markup)
  bot.register_next_step_handler(message, upgrageSteps, nextStep)


def WhatBaySteps(message, lastStep):

  if lastStep == 0:
    WBsChoiceCS(message, 'sChoiceCS')

  elif lastStep == 'sChoiceCS':
    if message.text == 'text1':
      WBChest1(message, 'C1choice')
    elif message.text == 'text2':
      WBSkins1(message, 'S1choice')

  elif lastStep == 'C1choice':
    if message.text == 'Подробнее':
      WBmore(message)
      menuBtn(message)
    elif message.text == 'В меню':
      menu(message)

  elif lastStep == 'S1choice':
    if message.text == 'Предложить свой':
      bot.register_next_step_handler(
          message,
          WBAddOffer,
      )
    elif message.text == 'В меню':
      menu(message)


def WBsChoiceCS(message, stepName):
  markup = types.ReplyKeyboardMarkup()
  btn1 = types.KeyboardButton("text1")
  btn2 = types.KeyboardButton("text2")
  markup.row(btn1)
  markup.row(btn2)

  bot.send_message(message.chat.id, "Покупаем", reply_markup=markup)
  bot.register_next_step_handler(message, WhatBaySteps, stepName)


def WBChest1(message, stepName):
  photo = 'url'
  bot.send_photo(message.chat.id, photo)
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  btn1 = types.KeyboardButton("Подробнее")
  btn2 = types.KeyboardButton("В меню")
  markup.row(btn1)
  markup.row(btn2)

  bot.send_message(
      message.chat.id,
      "msg",
      reply_markup=markup)
  bot.register_next_step_handler(message, WhatBaySteps, stepName)


def WBSkins1(message, stepName):
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  btn1 = types.KeyboardButton("Предложить свой")
  btn2 = types.KeyboardButton("В меню")
  markup.row(btn1)
  markup.row(btn2)

  bot.send_message(
      message.chat.id,
      "info",
      reply_markup=markup)
  bot.register_next_step_handler(message, WhatBaySteps, stepName)


def WBAddOffer(message):
  firstname = message.from_user.first_name
  username = message.from_user.username
  offer = message.text.strip()

  bot.send_message(
      chatID, "Add offer: ('%s', '%s', '%s', '%s', '%s')" %
      (time.time(), str(datetime.now()), firstname, username, offer))
  bot.send_message(message.chat.id,
                   "Спасибо за предложение, позже добавлю в бота.")
  menu(message)


def WBmore(message):
  photo = 'url'
  bot.send_photo(message.chat.id, photo)
  bot.send_message(
      message.chat.id,
      "msg"
  )

token = 'BotToken'
bot = telebot.TeleBot(token)
Money = money()
chatID = 'ID notification chat'
priceUnlim = 500
priceDay = 5

@bot.message_handler(commands=['start'])
def start_message(message):

  firstname = message.from_user.first_name
  username = message.from_user.username

  bot.send_message(
      chatID, "('%s', '%s', '%s', '%s', '%s')" %
      (time.time(), str(datetime.now()), firstname, username, 'New client'))

  # Init markup
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  item1 = types.KeyboardButton("Да")
  item2 = types.KeyboardButton("Нет")
  markup.row(item1)
  markup.row(item2)

  #init message
  bot.send_message(
      message.chat.id,
      'Привет, это бот'
  )
  bot.send_message(message.chat.id,
                   'msg',
                   reply_markup=markup)
  bot.register_next_step_handler(message, CheckKnow)


def CheckKnow(message):
  if message.text == 'Да':
    bot.send_message(message.chat.id,
                     "Супер, тогда вы можете выбрать то, что вам интересно.")
    menu(message)
  else:
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btnNext = types.KeyboardButton("Продолжить")
    markup.row(btnNext)
    bot.send_message(
        message.chat.id,
        "info",
        reply_markup=markup)
    bot.register_next_step_handler(message, next1)


def next1(message):
  bot.send_message(message.chat.id,
                   "Супер, тогда вы можете выбрать то, что вам интересно.")
  menu(message)


def menu(message):
  markup = types.InlineKeyboardMarkup()
  connAuto = types.InlineKeyboardButton('Подключить',
                                        callback_data='connAuto')
  outI = types.InlineKeyboardButton('info', callback_data='outI')
  howManyI = types.InlineKeyboardButton('info',
                                        callback_data='howManyI')
  upgradeI = types.InlineKeyboardButton('info', callback_data='upgradeI')
  whatBayI = types.InlineKeyboardButton('info',
                                        callback_data='whatBayI')

  markup.row(connAuto)
  markup.row(outI, upgradeI)
  markup.row(howManyI, whatBayI)

  bot.send_message(message.chat.id, 'Меню', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
  if callback.data == 'connAuto':
    clickerConnectSteps(callback.message, 0)
  elif callback.data == 'outI':
    outI(callback.message)
  elif callback.data == 'howManyI':
    howMany(callback.message)
  elif callback.data == 'upgradeI':
    upgrageSteps(callback.message, 0)
  elif callback.data == 'whatBayI':
    WhatBaySteps(callback.message, 0)

  elif callback.data == 'testAC':
    clickerConnectSteps(callback.message, 'menu', 'testAC')
  elif callback.data == 'timeCon':
    clickerConnectSteps(callback.message, 'menu', 'timeCon')
  elif callback.data == 'bayUnlim':
    clickerConnectSteps(callback.message, 'menu', 'bayUnlim')
  elif callback.data == 'back':
    menu(callback.message)


def menuBtn(message):
  markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
  btnNext = types.KeyboardButton("Да")
  markup.row(btnNext)
  bot.send_message(message.chat.id, "Вернуться в меню?", reply_markup=markup)
  bot.register_next_step_handler(message, menu)

bot.infinity_polling()