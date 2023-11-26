#!/usr/bin/env bash

############################################################
###                                                      ###
###            Скрипт установки GigaShell                ###
###                                                      ###
###           Напиши ./install.bash --install            ###
###                                                      ###
############################################################

function install {

[ -x `which python` ] || { echo "Не обнаружен Python! Установка прервана" && exit 1 ; }

echo Устанавливаем модули Python...
pip install -q gigachat  2> /dev/null || { echo "Не удалось установить библиотеку gigachat! Установка прервана" && exit 1 ; }
pip install -q langchain 2> /dev/null || { echo "Не удалось установить библиотеку langchain! Установка прервана" && exit 1 ; }

echo Устанавливаем GigaShell...
sudo cp gigashell.py /usr/local/bin
sudo ln -s /usr/local/bin/gigashell.py /usr/local/bin/gigashell
sudo chmod +x /usr/local/bin/gigashell.py
sudo ln -s /usr/local/bin/gigashell.py /usr/local/bin/gs

[ -x /usr/local/bin/gigashell ] || { echo "Что-то пошло не так! Установка прервана" && exit 1 ; }

echo Ура! GigaShell установлен!
[ `env | grep GIGACHAT_CREDENTIALS` ] || echo Не забудь также прописать токен в переменную GIGACHAT_CREDENTIALS
}

case $1 in
  "--install" ) install ;;
            * ) echo "Напиши ./install.bash --install" ;;
esac

