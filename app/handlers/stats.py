import os
from datetime import datetime, timedelta, timezone
from telegram import Update
from telegram.ext import ContextTypes
from sqlalchemy import select, func
from app.db.session import async_session
from app.db.models import TelegramUser

ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None or update.message is None: return

    if user.id != ADMIN_ID: return

    async with async_session() as session:
        total = await session.scalar(
            select(func.count()).select_from(TelegramUser)
        )
        active_7d = await session.scalar(
            select(func.count()).where(
                TelegramUser.last_active >= datetime.now(timezone.utc) - timedelta(days=7)
            )
        )

    await update.message.reply_text(
        f"👥 إجمالي المستخدمين: {total}\n"
        f"🟢 نشطون آخر 7 أيام: {active_7d}"
    )