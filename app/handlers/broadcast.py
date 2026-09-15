import os
import asyncio
from telegram import Bot, Update
from telegram.ext import ContextTypes
from telegram.error import Forbidden, BadRequest
from sqlalchemy import select
from app.db.session import async_session
from app.db.models import TelegramUser
from app.core.logger import setup_logger

logger = setup_logger()
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))


async def broadcast_to_all(bot: Bot, text: str, parse_mode: str = "HTML") -> tuple[int, int]:
    """يرجع (عدد النجاح, عدد الفشل)"""
    async with async_session() as session:
        result = await session.execute(select(TelegramUser.id))
        user_ids = [row[0] for row in result.all()]

    success, failed = 0, 0
    for uid in user_ids:
        try:
            await bot.send_message(uid, text, parse_mode=parse_mode)
            success += 1
        except Forbidden:
            # المستخدم حظر البوت أو حذف حسابه
            failed += 1
            logger.info(f"User {uid} blocked the bot, skipping.")
        except BadRequest as e:
            failed += 1
            logger.warning(f"BadRequest sending to {uid}: {e}")

        await asyncio.sleep(0.05)  # احترام حدود تليجرام (~30 رسالة/ثانية)

    return success, failed


async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user is None or update.message is None:
        return
    if user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("الاستخدام: /broadcast نص الرسالة هنا")
        return

    text = " ".join(context.args)
    await update.message.reply_text("⏳ جاري الإرسال...")

    success, failed = await broadcast_to_all(context.bot, text)

    await update.message.reply_text(
        f"✅ تم الإرسال\nنجح: {success}\nفشل: {failed}"
    )