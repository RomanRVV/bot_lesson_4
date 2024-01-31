# quiz
Проект создан для провидения викторин с использованием чат-ботов Telegram и VK.

Ссылки на группу [ВК](https://vk.com/club223682986) и [Телеграмм бота](https://t.me/ROMANRV_test_bot)

## Как установить
Для запуска скрипта вам понадобится Python 3.10

Скачайте код с GitHub. Затем установите зависимости

```sh
pip install -r requirements.txt
```
## Переменные окружения

Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в репозитории и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

- `TG_API_TOKEN` — Telegram token ([инструкция по созданию бота и получению токена](https://way23.ru/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B1%D0%BE%D1%82%D0%B0-%D0%B2-telegram.html))
- `VK_API_TOKEN` — VK token группы ([инструкция](https://uchet-jkh.ru/i/gde-naxoditsya-token-gruppy-vkontakte/))
- `REDIS_HOST` — Хост базы данных [Redis](https://redis.com/)
- `REDIS_PORT` — Порт базы данных [Redis](https://redis.com/)
- `REDIS_PASSWORD` — Пароль от базы данных [Redis](https://redis.com/)

## Как запустить

Зарегистрируйтесь на сайте Redis и создайте базу данных 


Запуск вк и телеграмм ботов

```
python tg_bot.py
python vk_bot.py
```


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
