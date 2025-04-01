import asyncio
import csv
import os
import codecs
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from config import API_ID, API_HASH, PHONE, SESSION_NAME

async def main():
    # Инициализация клиента
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start(phone=PHONE)
    
    print("Получение списка всех диалогов...")
    print("-" * 50)
    
    # Получаем расширенный список диалогов через API запрос
    result = await client(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=500,  # Увеличиваем лимит для получения большего числа чатов
        hash=0
    ))
    
    # Создаем словари для группировки по типам
    users = []
    groups = []
    channels = []
    
    # Заполняем списки
    for dialog in result.dialogs:
        entity = await client.get_entity(dialog.peer)
        
        # Определяем тип и добавляем в соответствующий список
        chat_id = entity.id  # Используем ID из entity, а не из dialog
        
        try:
            title = entity.title if hasattr(entity, 'title') else (
                f"{entity.first_name} {entity.last_name}" if hasattr(entity, 'first_name') else str(entity.id)
            )
        except:
            title = "Неизвестное имя"
        
        # Получаем username, если есть
        username = entity.username if hasattr(entity, 'username') and entity.username else "Нет"
        
        # Получаем информацию о количестве участников для групп и каналов
        members_count = "Неизвестно"
        try:
            if hasattr(entity, 'megagroup') or hasattr(entity, 'broadcast'):
                full_chat = await client.get_entity(entity)
                if hasattr(full_chat, 'participants_count'):
                    members_count = full_chat.participants_count
        except:
            pass
        
        # Добавляем дополнительную информацию
        chat_info = {
            'id': chat_id,
            'title': title,
            'username': username,
            'members': members_count,
            'verified': getattr(entity, 'verified', False),
            'restricted': getattr(entity, 'restricted', False),
            'scam': getattr(entity, 'scam', False),
            'fake': getattr(entity, 'fake', False),
            'access_hash': getattr(entity, 'access_hash', 'Нет')
        }
        
        if hasattr(entity, 'megagroup') and entity.megagroup:
            chat_info['type'] = 'Супергруппа'
            groups.append(chat_info)
            print(f"Супергруппа: {title} (@{username}) ID: {chat_id}")
        elif hasattr(entity, 'broadcast') and entity.broadcast:
            chat_info['type'] = 'Канал'
            channels.append(chat_info)
            print(f"Канал: {title} (@{username}) ID: {chat_id}")
        elif hasattr(entity, 'first_name'):
            chat_info['type'] = 'Пользователь'
            users.append(chat_info)
            print(f"Пользователь: {title} (@{username}) ID: {chat_id}")
        else:
            chat_info['type'] = 'Группа'
            groups.append(chat_info)
            print(f"Группа: {title} (@{username}) ID: {chat_id}")
    
    # Сохраняем в CSV файл с расширенной информацией с BOM-маркером для корректного отображения в Excel
    filename = 'telegram_chats.csv'
    with codecs.open(filename, 'w', 'utf-8-sig') as csvfile:
        fieldnames = ['Тип', 'Название', 'Username', 'ID', 'Участники', 'Верифицирован', 'Ограничен', 'Скам', 'Фейк', 'Access Hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Сначала пользователи
        for user in users:
            writer.writerow({
                'Тип': user['type'],
                'Название': user['title'],
                'Username': user['username'],
                'ID': user['id'],
                'Участники': 'N/A',
                'Верифицирован': user['verified'],
                'Ограничен': user['restricted'],
                'Скам': user['scam'],
                'Фейк': user['fake'],
                'Access Hash': user['access_hash']
            })
        
        # Затем группы
        for group in groups:
            writer.writerow({
                'Тип': group['type'],
                'Название': group['title'],
                'Username': group['username'],
                'ID': group['id'],
                'Участники': group['members'],
                'Верифицирован': group['verified'],
                'Ограничен': group['restricted'],
                'Скам': group['scam'],
                'Фейк': group['fake'],
                'Access Hash': group['access_hash']
            })
        
        # Затем каналы
        for channel in channels:
            writer.writerow({
                'Тип': channel['type'],
                'Название': channel['title'],
                'Username': channel['username'],
                'ID': channel['id'],
                'Участники': channel['members'],
                'Верифицирован': channel['verified'],
                'Ограничен': channel['restricted'],
                'Скам': channel['scam'],
                'Фейк': channel['fake'],
                'Access Hash': channel['access_hash']
            })
    
    print("-" * 50)
    print(f"Всего найдено:")
    print(f"Пользователей: {len(users)}")
    print(f"Групп: {len(groups)}")
    print(f"Каналов: {len(channels)}")
    print(f"Данные сохранены в файл: {os.path.abspath(filename)}")
    print("Используйте полученный ID в параметре TARGET_CHAT в файле config.py")
    
    # Также сохраняем в отдельные файлы
    filenames = []
    
    if users:
        users_file = 'telegram_users.csv'
        with codecs.open(users_file, 'w', 'utf-8-sig') as csvfile:
            fieldnames = ['Название', 'Username', 'ID', 'Верифицирован', 'Ограничен', 'Скам', 'Фейк', 'Access Hash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for user in users:
                writer.writerow({
                    'Название': user['title'],
                    'Username': user['username'],
                    'ID': user['id'],
                    'Верифицирован': user['verified'],
                    'Ограничен': user['restricted'],
                    'Скам': user['scam'],
                    'Фейк': user['fake'],
                    'Access Hash': user['access_hash']
                })
        filenames.append(users_file)
    
    if groups:
        groups_file = 'telegram_groups.csv'
        with codecs.open(groups_file, 'w', 'utf-8-sig') as csvfile:
            fieldnames = ['Тип', 'Название', 'Username', 'ID', 'Участники', 'Верифицирован', 'Ограничен', 'Access Hash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for group in groups:
                writer.writerow({
                    'Тип': group['type'],
                    'Название': group['title'],
                    'Username': group['username'],
                    'ID': group['id'],
                    'Участники': group['members'],
                    'Верифицирован': group['verified'],
                    'Ограничен': group['restricted'],
                    'Access Hash': group['access_hash']
                })
        filenames.append(groups_file)
    
    if channels:
        channels_file = 'telegram_channels.csv'
        with codecs.open(channels_file, 'w', 'utf-8-sig') as csvfile:
            fieldnames = ['Название', 'Username', 'ID', 'Участники', 'Верифицирован', 'Ограничен', 'Access Hash']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for channel in channels:
                writer.writerow({
                    'Название': channel['title'],
                    'Username': channel['username'],
                    'ID': channel['id'],
                    'Участники': channel['members'],
                    'Верифицирован': channel['verified'],
                    'Ограничен': channel['restricted'],
                    'Access Hash': channel['access_hash']
                })
        filenames.append(channels_file)
    
    if filenames:
        print("Также данные сохранены в отдельных файлах по категориям:")
        for file in filenames:
            print(f"- {file}")
    
    # Закрываем соединение
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 