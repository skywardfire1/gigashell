#!/usr/bin/env python

# Всякие импорты
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import platform
import os
import argparse

def parse_arguments():
  parser = argparse.ArgumentParser( prog='gigashell',
                                    description='Sber GigaChat в твоей консоли!',
                                    epilog='Возрадуемся же!' )
  parser.add_argument( 'request', metavar = 'ЗАПРОС', help = 'Запрос к GigaChat' )
  group = parser.add_mutually_exclusive_group()
  group.add_argument( '-s', '--shell', help = 'Сгенерировать только финальную команду', action = 'store_true' )
  group.add_argument( '-c', '--chat', nargs = 1, action = 'store', help = 'Название для чата' )
  group.add_argument( '-l', '--list-chats', action = 'store_true', help = 'Список чатов' )
  # Здесь возвращаем сразу результат возврата функции
  return parser.parse_args()


# СБОР ДАННЫХ О СИСТЕМЕ
def dist():
  try:
    return platform.dist()
  except:
    return 'Неизвестный'

def make_prompt():
  system_os = platform.system()
  system_architecture = platform.machine()
  system_distibutive = dist()
  shell_name = os.readlink('/proc/%d/exe' % os.getppid())

  # Собираем разогревочный промт
  warmup_prompt = f'Ты бот помощник, запущенный на операционной системе {system_os} {system_distibutive}. Архитектура системы {system_architecture}. Прямо сейчас пользователь работает в командной оболочке {shell_name}. Отвечай на вопрос с учётом этих данных. Не выводи никаких приветствий и рассказов о своих ограничениях.'

  # Если включен флаг -s, то скрипт должен вывести только лишь команду, без объяснений
  if arguments.shell:
    warmup_prompt = warmup_prompt + ' ' + 'Будь краток. Выведи только команду для оболочки {shell_name} операционной системы {system_os}, и больше ничего. Никаких дополнительных объяснений. Больше ничего в твоём ответе не должно быть, только финальная команда. Выведи только команду, без тэгов markdown. Команда должна быть готова к выполнению без дополнительных правок. Если тебе недостаточно данных, предоставь наиболее логичное решение. Все перечисленные требования обязательны к выполнению. Без исключений. Все перечисленные требования обязательны к выполнению, без исключений.'
  else:
    warmup_prompt = warmup_prompt + ' ' + 'Отвечай на вопрос развёрнуто, с объяснениями'

  return warmup_prompt

def init_chat():
  if not os.path.exists( '~/.gigashell/chats' ):
    mkdir( '~/.gigashell/chats' )
  else:
    return False

#def do_continuous_request( chat_name ):



# В функцию надо передать запрос от пользователя
def do_request( system_message, request_text ):
  # Авторизация в сервисе GigaChat
  #chat = GigaChat( credentials=<авторизационные_данные>, verify_ssl_certs=False)
  chat = GigaChat( verify_ssl_certs=False)
  messages = [ SystemMessage( content = system_message ), HumanMessage( content = request_text ) ]
  res = chat( messages )
  # messages.append(res)
  print( res.content )

#  print( f'messages полностью: {messages}' )
#  print( f"res полностью: {res}" )
  return 0

if __name__ == '__main__':
  # Парсим аргументы
  arguments = parse_arguments()
  do_request( make_prompt(), arguments.request )


