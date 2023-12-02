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


def parse_arguments():
    parser = argparse.ArgumentParser( prog='gigashell',
                                    description='Sber GigaChat в твоей консоли!',
                                    epilog='Нейросеть в твоем терминале' )
    parser.add_argument( 'request', metavar = 'ЗАПРОС', nargs = '?', default = '', help = 'Запрос к GigaChat' )
    group = parser.add_mutually_exclusive_group()
    group.add_argument( '-s', '--shell', action = 'store_true', help = 'Сгенерировать только финальную команду. Имеет смысл только совместно с запросом' )
    # TODO group.add_argument( '-c', '--chat', nargs = 1, action = 'store', help = 'Название для чата' )
    # TODO group.add_argument( '-l', '--list-chats', action = 'store_true', help = 'Список чатов' )
    group.add_argument( '-v', '--version', action = 'store_true', help = 'Вывести информацию о версии, и закончить работу' )
    # Здесь возвращаем сразу результат возврата функции
    return parser.parse_args()


def get_size(bytes: int, suffix: str='B') -> str:
	"""Получаем размер из байтов в более большие форматы. Доступны:
	килобайты, мегабайты, гигабайты, терабайты, петабайты.
	Аргументы:
	 + bytes: int - количество байтов
	 + suffix: str - тип суффикса
	Возвращает:
	 + str - размер"""
	factor = 1024

	for unit in ["", "K", "M", "G", "T", "P"]:
		if bytes < factor:
			return f'{bytes:.2f}{unit}{suffix}'
		bytes /= factor


def print_log(text: str) -> None:
	"""Вывод на экран строки
	Аргументы:
	 + text: str - текст для вывода"""
	print(text)


class ResourceMonitor:
	"""Монитор системных ресурсов компьютера"""
	def __init__(self):
		# Инициализация объекта - создание переменных
		self.uname = platform.uname()
		self.cpufreq = psutil.cpu_freq()
		self.swap = psutil.swap_memory()
		self.svmem = psutil.virtual_memory()
		self.partitions = psutil.disk_partitions()
		self.if_addrs = psutil.net_if_addrs()
		self.net_io = psutil.net_io_counters()

	def call_all(self):
		# Вызов всех функций
		self.system_info()
		self.proc_info()
		self.ram_info()
		self.disk_info()
		self.network_info()

	def system_info(self):
		# Общая информация о системе
		print('=' * 10, 'Информация о системе', '=' * 10)
		logging.info('Информация о системе')
		print_log(f'Система: {self.uname.system}')
		print_log(f'Имя сетевого узла: {self.uname.node}')
		print_log(f'Выпуск: {self.uname.release}')
		print_log(f'Версия: {self.uname.version}')
		print_log(f'Машина: {self.uname.machine}')
		print_log(f'Процессор: {self.uname.processor}')

	def proc_info(self):
		# Информация о процессоре
		print('=' * 10, 'Информация о процессоре', '=' * 10)
		logging.info('Информация о процессоре')
		print_log(f'Физические ядра: {psutil.cpu_count(logical=False)}')
		print_log(f'Количество ядер: {psutil.cpu_count(logical=True)}')
		print_log(f'Маскимальная частота процессора: {self.cpufreq.max:.2f}МГц')
		print_log(f'Минимальная частота процессора: {self.cpufreq.min:.2f}МГц')
		print_log(f'Текущая частота процессора: {self.cpufreq.current:.2f}МГц')
		for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
			print_log(f'Загруженность ядра {i}: {percentage}%')
		print_log(f'Общая загруженность процессора: {psutil.cpu_percent()}%')

	def network_info(self):
		# Информация о сети
		print('=' * 10, 'Информация о сети', '=' * 10)
		logging.info('Информация о сети')
		for inteface_name, interface_addresses in self.if_addrs.items():
			for address in interface_addresses:
				print('=' * 5, f'Информация о интерфейсе сети: {inteface_name}', '=' * 5)
				logging.info(f'Информация о интерфейсе сети: {inteface_name}')
				if str(address.family) == 'AddressFamily.AF_INET':
					print_log(f'Тип интерфейса сети {inteface_name}: {str(address.family)}')
					print_log(f'IP интерфейса сети {inteface_name}: {address.address}')
					print_log(f'Сетевая маска интерфейса сети {inteface_name}: {address.netmask}')
					print_log(f'Широковещательный IP-адрес интерфейса сети {inteface_name}: {address.broadcast}')
				elif str(address.family) == 'AddressFamily.AF_PACKET':
					print_log(f'Тип интерфейса сети {inteface_name}: {str(address.family)}')
					print_log(f'MAC-адрес интерфейса сети {inteface_name}: {address.address}')
					print_log(f'Сетевая маска интерфейса сети {inteface_name}: {address.netmask}')
					print_log(f'Широковещательный IP-адрес интерфейса сети {inteface_name}: {address.broadcast}')
				else:
					print_log(f'Тип интерфейса сети {inteface_name}: {str(address.family)}')
					print_log(f'MAC-адрес интерфейса сети {inteface_name}: {address.address}')
					print_log(f'Сетевая маска интерфейса сети {inteface_name}: {address.netmask}')
					print_log(f'Широковещательный IP-адрес интерфейса сети {inteface_name}: {address.broadcast}')
		print_log(f'Общее количество отправленных байтов: {get_size(self.net_io.bytes_sent)}')
		print_log(f'Общее количество полученных байтов: {get_size(self.net_io.bytes_recv)}')

	def disk_info(self):
		# Информация о разделах диска
		print('=' * 10, 'Информация о дисках', '=' * 10)
		logging.info('Информация о дисках')
		for partition in self.partitions:
			print('=' * 5, f'Информация о разделе диска: {partition.device}', '=' * 5)
			logging.info(f'Информация о разделе диска: {partition.device}')
			print_log(f'Файловая система раздела диска {partition.device}: {partition.fstype}')
			try:
				partition_usage = psutil.disk_usage(partition.mountpoint)
			except PermissionError:
				continue
			print_log(f'Общий обьем раздела диска {partition.device}: {get_size(partition_usage.total)}')
			print_log(f'Используемый обьем раздела диска {partition.device}: {get_size(partition_usage.used)}')
			print_log(f'Свободный обьем раздела диска {partition.device}: {get_size(partition_usage.free)}')
			print_log(f'Процент объема раздела диска {partition.device}: {get_size(partition_usage.percent)}')

	def ram_info(self):
		# Информация об оперативной памяти и памяти подкачки
		print('=' * 10, 'Информация об ОЗУ', '=' * 10)
		logging.info('Информация об ОЗУ')
		print_log(f'Объем ОЗУ: {get_size(self.svmem.total)}')
		print_log(f'Доступно ОЗУ: {get_size(self.svmem.available)}')
		print_log(f'Используется ОЗУ: {get_size(self.svmem.used)}')
		print_log(f'Процент ОЗУ: {get_size(self.svmem.percent)}')
		if self.swap:
			print('=' * 5, 'Информация о памяти подкачки', '=' * 5)
			logging.info('Информация о памяти подкачки')
			print_log(f'Объем памяти подкачки: {get_size(self.swap.total)}')
			print_log(f'Свободно памяти подкачки: {get_size(self.swap.free)}')
			print_log(f'Используется памяти подкачки: {get_size(self.swap.used)}')
			print_log(f'Процент памяти подкачки: {self.swap.percent}%')


def start_pc_monitor():
	# Запускаем монитор ресурсов
	monitor = ResourceMonitor()
	monitor.call_all()


# Собираем данные о системе и составляем разогревочный промт
def make_prompt():
    system_os = platform.system()
    system_architecture = platform.machine()
    system_distributive = distro.name()
    distributive_version = distro.version()
    kernel_version = platform.release()
    shell_name = os.readlink('/proc/%d/exe' % os.getppid())

    warmup_prompt = f'Твоя задача отвечать на вопрос пользователя, который работает в операционной системе {system_os}, версия ядра {kernel_version}. Дистрибутив называется {system_distributive} {distributive_version}. Архитектура системы {system_architecture}. Оболочка {shell_name}.'
    # Если включен флаг -s, то скрипт должен вывести только лишь команду, без объяснений. Пока на данный момент работает плохо
    if arguments.shell:
        warmup_prompt += " {warmup_prompt}. Не пиши дополнительных объяснений. Напиши только одну команду. Нужна только одна команда. Не выводи тэгов code. Команда должна быть готова к выполнению без дополнительных правок. Если тебе недостаточно данных, предоставь наиболее логичное решение. Все перечисленные требования обязательны к выполнению. Без исключений. Все перечисленные требования обязательны к выполнению, без исключений. Ответь на вопрос кратко, одной командой."
    else:
        warmup_prompt += " {warmup_prompt}. Отвечай на вопрос развёрнуто, с объяснениями"

    print('Информация о вашей системе:')
    start_pc_monitor()

    return warmup_prompt

# В функцию надо передать запрос от пользователя
def do_request( system_message, request_text ):
    # Авторизация в сервисе GigaChat
    chat = GigaChat( verify_ssl_certs=False)
    messages = [ SystemMessage( content = system_message ), HumanMessage( content = request_text ) ]
    res = chat( messages )
    print( res.content )
    
    return 0

if __name__ == '__main__':
    # Парсим аргументы
    arguments = parse_arguments()

    if arguments.version:
        print( 'GigaShell, версия 0.1, 26 ноября 2023' )
        exit

    if not arguments.request == '': do_request( make_prompt(), arguments.request )
