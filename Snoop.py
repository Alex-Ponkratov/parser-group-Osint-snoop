from telethon import TelegramClient
from telethon.tl.types import User
from telethon.errors import SessionPasswordNeededError, FloodWaitError

# Учетные данные для авторизации
api_id = '23745953'  # Ваш api_id
api_hash = 'e91ece346bcab21f86b9becde177ceff'  # Ваш api_hash
phone_number = '+375447510814'  # Ваш номер телефона
channel = '@gogolang'  # Название или ID канала/чата

# Автоматическое создание имени файла на основе имени канала
output_file = f"{channel.replace('@', '')}_users.txt"

# Создаем клиент Telegram с сохранением сессии
client = TelegramClient('session_name', api_id, api_hash)


async def main():
    try:
        # Авторизация
        await client.start(phone=phone_number)

        if not await client.is_user_authorized():
            print("Не удалось авторизоваться.")
            return

        print(f"Сбор участников из чата: {channel}")

        # Получаем всех участников чата
        participants = await client.get_participants(channel)
        print(f"Получено {len(participants)} участников.")

        # Создаем список юзернеймов без @ в начале
        usernames = [user.username for user in participants if isinstance(user, User) and user.username]

        # Сохранение юзернеймов в файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(usernames))

        print(f"Сохранено {len(usernames)} юзернеймов в файл '{output_file}'.")

    except SessionPasswordNeededError:
        print("Необходимо ввести код двухфакторной аутентификации.")
    except FloodWaitError as e:
        print(f"Слишком много запросов. Подождите {e.seconds} секунд.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Запуск программы
with client:
    client.loop.run_until_complete(main())