from datetime import datetime, timezone
from telegram import Update
from telegram.ext import ContextTypes
from app.db.session import async_session
from app.db.models import TelegramUser
from app.core.logger import setup_logger

logger = setup_logger()

async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None:
        return
    try:
        async with async_session() as session:
            existing = await session.get(TelegramUser, user.id)
            if existing:
                existing.last_active = datetime.now(timezone.utc)
                existing.username = user.username
                existing.first_name = user.first_name
            else:
                session.add(TelegramUser(
                    id=user.id,
                    username=user.username,
                    first_name=user.first_name,
                ))
            await session.commit()
        logger.info(f"Tracked user {user.id} successfully.")

    except Exception as e:
        logger.error(f"Failed to track user {user.id}: {type(e).__name__}: {e}", exc_info=True)