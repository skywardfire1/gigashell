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
  parser.add_argument( '--shell', '-s', help = 'Сгенерировать только финальную команду', action = 'store_true' )
  parser.add_argument( '--prompt', '-p', help = 'Текст запроса', action = 'store', required = True )

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

# Готовим разогревочный промпт к передаче в API
#messages = [ SystemMessage( content = warmup_prompt ) ]

# В функцию надо передать запрос от пользователя
def do_request( request_text ):
  # Авторизация в сервисе GigaChat
  #chat = GigaChat( credentials=<авторизационные_данные>, verify_ssl_certs=False)
  chat = GigaChat( verify_ssl_certs=False)
  # Готовим разогревочный промпт к передаче в API

#  messages = [ SystemMessage( content = make_prompt() ) ]
#  messages.append( HumanMessage( content = request_text ) )
  messages = [ SystemMessage( content = make_prompt() ), HumanMessage( content = request_text ) ]
  res = chat( messages )
  # messages.append(res)
  print( res.content )
  return 0

if __name__ == '__main__':
  # Парсим аргументы
  arguments = parse_arguments()
  do_request( arguments.prompt )


