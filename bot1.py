import telebot;
import os
import time

bot=telebot.TeleBot("")
chatid=0
msginfo = 0
active=False



def init():
  global bot
  global chatid
  global msginfo
  global active
  
  if not(getToken()==""):
    bot = telebot.TeleBot(getToken())
    if not(getChatId()==""):
      chatid=getChatId()
      msginfo = bot.send_message(chatid, "Здарова")
      active=True
    else:print("Write /start to your bot!!!")
  else:print("bot does not work! please enter your token(--newbot ...)")



def setChatId(messages):
    if(getChatId()==""):
      bot.send_message(messages[0].chat.id, 'Поехали!!!')
      open('cfg/botchatid','w').write(str(messages[0].chat.id))
      print("Successful!!!")
      os.abort()
    else:
      bot.send_message(messages[0].chat.id, 'Моя тебя не понимать')

def send(text):
   if active:bot.send_message(chatid, text) 
def updateinfo(text):
   if active:
     global msginfo
     try:
        msginfo=bot.edit_message_text(chat_id=chatid, message_id=msginfo.message_id, text=text)
     except:print("")
def delmsg():
   if active:
     global msginfo
     bot.delete_message(msginfo.chat.id, msginfo.message_id)

def getChatId():
  try:
    return int(open('cfg/botchatid').read())
  except:
    return ""

def getToken():
  try:
    return open('cfg/bottoken').read()
  except:
    return ""
def setToken(token):
  global bot
  open('cfg/bottoken','w').write(token)
  print("Now send 'start' to your bot")
  bot=telebot.TeleBot(getToken())
  bot.set_update_listener(setChatId)
  bot.polling()
  



