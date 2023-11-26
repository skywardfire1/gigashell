
# GIGA
# SHELL

(https://cdn-app.sberdevices.ru/asset/sites_856/aHR0cHM6Ly9jZG4tYXBwLnNiZXJkZXZpY2VzLnJ1L21pc2MvMC4wLjAvYXNzZXRzL2NvbW1vbi8xMDEwNjhjZl9naWdhY2hhdC5wbmc=)


Привет! Ты сейчас находишься в репозитории gigashell, неофициальная утилита командной строки, с помощью которой можно легко и быстро прикрутить современную нейросеть к твоей линукс-консоли.

Предварительно надо получить токен, это можно сделать **[вот тут](https://developers.sber.ru/portal/products/gigachat-api)**

Потом этот токен должен храниться в переменной окружения GIGACHAT_CREDENTIALS

Например, можно прописать соответствующий export в файл .bashrc в домашней директории пользователя, под которым работаешь. Хоть это и не самый секюрный способ.

## Настраиваем авторизацию в сервисе

```sh
echo "\n" > ~/.bashrc
echo "export GIGACHAT_CREDENTIALS=ТОКЕН >> ~/.bashrc
```

Если используешь ZSH, то файл будет называться .zshrc

## Установка

Установка проста:

```sh
git clone https://github.com/skywardfire1/gigashell.git
./install.bash --install
```
