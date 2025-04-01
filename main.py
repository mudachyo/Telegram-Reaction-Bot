import asyncio
import random
import logging
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendReactionRequest
from telethon.tl.types import ReactionEmoji, User
from config import API_ID, API_HASH, PHONE, SESSION_NAME, TARGET_CHAT

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Основная реакция
MAIN_REACTION = "❤"  # Используем одинарный символ сердца

async def main():
    # Инициализация клиента
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    
    @client.on(events.NewMessage(chats=TARGET_CHAT))
    async def handler(event):
        try:
            # Проверяем, что сообщение не от бота (корректная проверка типа объекта)
            sender = await event.get_sender()
            
            if isinstance(sender, User) and sender.bot:
                logger.info(f"Пропускаем сообщение от бота @{sender.username}")
                return
            
            # Получаем и выводим текст сообщения
            message_text = event.message.message if event.message.message else "[Медиа или другой контент]"
            
            # Безопасное получение имени отправителя
            sender_name = ""
            if hasattr(sender, 'first_name') and sender.first_name:
                sender_name += sender.first_name + " "
            if hasattr(sender, 'last_name') and sender.last_name:
                sender_name += sender.last_name
                
            sender_name = sender_name.strip()
            
            if not sender_name and hasattr(sender, 'title') and sender.title:
                sender_name = sender.title
            
            if not sender_name:
                sender_name = "Неизвестный отправитель"
            
            logger.info(f"Новое сообщение от {sender_name}: {message_text[:100]}...")
                
            # Добавляем небольшую случайную задержку перед отправкой реакции (2-5 секунд)
            delay = random.uniform(2.0, 5.0)
            logger.info(f"Ждем {delay:.1f} секунд перед добавлением реакции...")
            await asyncio.sleep(delay)
            
            # Отправляем только одну реакцию - сердечко
            logger.info(f"Добавляем реакцию {MAIN_REACTION}")
            
            await client(SendReactionRequest(
                peer=event.chat_id,
                msg_id=event.message.id,
                reaction=[ReactionEmoji(emoticon=MAIN_REACTION)]
            ))
            
        except Exception as e:
            logger.error(f"Ошибка при добавлении реакции: {e}")
            logger.exception("Детали ошибки:")
    
    await client.start(phone=PHONE)
    logger.info(f"Мониторинг чата {TARGET_CHAT} начат. Нажмите Ctrl+C для остановки.")
    logger.info(f"Бот будет ставить реакцию {MAIN_REACTION} на новые сообщения")
    logger.info(f"Сообщения от ботов будут игнорироваться")
    
    # Запускаем клиент до тех пор, пока не будет прерван
    await client.run_until_disconnected()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Скрипт остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        logger.exception("Детали критической ошибки:")
