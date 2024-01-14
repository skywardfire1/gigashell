#!/usr/bin/env python

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat
import platform
import os
import argparse
import sys
from datetime import datetime
import psutil
import distro
import pickle

def parse_arguments():
    parser = argparse.ArgumentParser( prog='gigashell', description='Sber GigaChat в твоей консоли!', epilog='Возрадуемся же!' )
    parser.add_argument( '-L', '--last-message', action = 'store_true', help = 'Включить в запрос предыдущее сообщение' )

    group_v_r = parser.add_mutually_exclusive_group()
    group_v_r.add_argument( 'request', metavar = 'ЗАПРОС', nargs = '?', default = '', help = 'Запрос к GigaChat' )
    group_v_r.add_argument( '-v', '--version', action = 'store_true', help = 'Вывести информацию о версии, и закончить работу' )

    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument( '-s', '--shell', action = 'store_true', help = 'Сгенерировать только финальную команду. Имеет смысл только совместно с запросом' )
    group_2.add_argument( '-p', '--system-prompt', action = 'store', default = 'no_custom_prompt_provided', help = 'Задать свой собственный системный промт' )
    group_2.add_argument( '-m', '--more-info', action = 'store_true', help = 'Добавить в запрос больше информации о системе' )
    return parser.parse_args()

# Больше данных о системе
def prompt_data_cpu():
    # Физические ядра пока не включаю в запрос, но на всякий случай оставлю тут {psutil.cpu_count(logical=False)}')
    info = f'Количество ядер: {psutil.cpu_count(logical=True)}.'
    info += f' Маскимальная частота: {psutil.cpu_freq().max:.2f}МГц.'
    info += f' Минимальная частота: {psutil.cpu_freq().min:.2f}МГц.'
    info += f' Текущая частота: {psutil.cpu_freq().current:.2f}МГц.'
    return info

def prompt_data_network_iface():
    if_addrs = psutil.net_if_addrs()

    info = f'Имеются следующие сетевые интерфейсы:'

    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
          if str(address.family) == 'AddressFamily.AF_INET':
            info += f' Имя интерфейса: {interface_name}, тип: {str(address.family)}, адрес: {address.address}, маска сети: {address.netmask}.'
          if str(address.family) == 'AddressFamily.AF_PACKET':
            info += f' Имя интерфейса: {interface_name}, тип: {str(address.family)}, адрес: {address.address}, маска сети: {address.netmask}.'
    return info

# Собираем данные о системе и составляем разогревочный промт
def make_prompt():
    # Обрабатываем опцию -p. Если пользователь задал собственный системный промт, иcпользуем его
    if arguments.system_prompt != 'no_custom_prompt_provided': return arguments.system_prompt


    system_os = platform.system()
    system_architecture = platform.machine()
    system_distributive = distro.name()
    distributive_version = distro.version()
    kernel_version = platform.release()
    shell_name = os.readlink('/proc/%d/exe' % os.getppid())

    # Поэтапно составляем промт
    warmup_prompt = ''

    # Если задан флаг -s, то промт надо начать именно так
    if arguments.shell: warmup_prompt = 'Выведи команду, которая позволит ответить на вопрос пользователя. Напиши только одну команду. Не выводи никаких дополнительных пояснений.'

    # Этот блок присоединяется в любом случае
    warmup_prompt += f' Пользователь работает в операционной системе {system_os}, версия ядра {kernel_version}. Дистрибутив называется {system_distributive} {distributive_version}. Архитектура системы {system_architecture}. Оболочка {shell_name}.'

    # Флаг -m вполне совместим со всем предыдущим, можем добавить больше инфы о системе
    if arguments.more_info: warmup_prompt += f'Информация о процессорах: {prompt_data_cpu()}. Информация о сетевых интерфейсах: {prompt_data_network_iface()}'

    return warmup_prompt

# Для чатов
def store_message( message ):
    file_name = '/tmp/gigachat_last_message'
    with open( file_name, 'wb' ) as db_file:
      pickle.dump( message, db_file )
    return 0

def get_message():
    file_name = '/tmp/gigachat_last_message'
    try:
      with open( file_name, 'rb' ) as db_file:
        message = pickle.load( db_file )
      return message
    except:
      return ''

def do_request( request_text ):
    # Авторизация в сервисе GigaChat
    chat = GigaChat( verify_ssl_certs = False )

    system_message = SystemMessage( content = make_prompt() )
    user_message = HumanMessage( content = request_text )

    if arguments.last_message:
      messages = get_message()
      if messages == '':
        messages = [ system_message, user_message ]
      else:
        messages.append( user_message )
    else:
      messages = [ system_message, user_message ]

    res = chat( messages )

    print( res.content )
    messages.append( res )
    store_message( messages )

    return 0

if __name__ == '__main__':
    # Парсим аргументы
    arguments = parse_arguments()

    if arguments.version:
      print( 'GigaShell, версия 0.2, 1 января 2023' )
      exit(0)

    do_request( arguments.request )

