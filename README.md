# SUPPORT BOT

Боты, которые отвечают на базовые вопросы пользователей с помощью Dialogflow.

Пример работы бота [Telegram (нажмите)]("https://t.me/chelobbot"):

![Пример работы Telegram бота.](https://dvmn.org/filer/canonical/1569214094/323/)

Пример работы бота [VK (нажмите)]("https://vk.com/im?sel=-214882658"):

![Пример работы VK бота.](https://dvmn.org/filer/canonical/1569214089/322/)
## Как запустить 
- Для запуска библиотеки у вас уже должен быть установлен [Python 3](https://www.python.org/downloads/).
- Установите зависимости командой:
```
pip install -r requirements.txt
```
- Настроить переменные окружения.
- Запустите [telegram](https://telegram.org/) бота  командой:
```
python tg_bot.py
```
- Запустить [VK](https://vk.com/) бота:
```
python vk_bot.py
```

## Переменные окружения
Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл .env рядом в корне проекта и запишите туда данные в таком формате: ПЕРЕМЕННАЯ=значение.

Необходимы следущие переменные:
- `TELEGRAM_TOKEN` — Telegram token вашего бота, для получения нужно написать @BotFather в телеграме.
- `VK_TOKEN` — VK token c возможностью отправлять сообщения. Как [получить](https://pechenek.net/social-networks/vk/api-vk-poluchaem-klyuch-dostupa-token-gruppy/).
- `GOOGLE_APPLICATION_CREDENTIALS` – путь до вашего JSON ключа от google aplication. Как [получить](https://cloud.google.com/docs/authentication/getting-started).
## Загрузка Intent'ов
Для того чтобы загрузить intent'ы вам нужно:
1. Создать файл формата json.
2. Внутри файла написать структуру:
```
{
    "Отображаемое имя intent'a": {
        "questions": [
            "Здесь",
            "Пишите",
            "Training phrases",
            ...
        ],
        "answer": "Напишите ответ."
    },
    ...
}
```
`answer` может быть указан несколькими вариантами, так:
```
"answer": "Напишите ответ."
```
Или так:
```
"answer": [
            "Напишите ответ.",
            "Напишите ответ.",
            ...
        ],
```
3. напишите команду:
```
python dialogflow.py file-name.json
```