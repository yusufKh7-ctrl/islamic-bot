from telegram import Update, BotCommand, ReplyKeyboardMarkup
from telegram.request import HTTPXRequest
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters
)
from app.core.logger import setup_logger
from app.data.ayah import get_random_ayah
from app.data.hadith import get_random_hadith, get_random_hadith_qudsi
from app.data.adhkar import morning_adhkar, evening_adhkar, general_adhkar
from app.data.quran_dua import get_random_dua


import os
from dotenv import load_dotenv


load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not exists!")

logger = setup_logger()

# ======= /start =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    assert user is not None
    username = user.username
    user_display = username if username else user.full_name

    keyboard = [
        ["📖 آية من القرآن", "🤲 دعاء من القرآن"],
        ["📜 حديث شريف", "✍️ حديث قُدسي"],
        ["💭 ذكر من الأذكار"],
        ["🌅 أذكار الصباح", "🌙 أذكار المساء"],
    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True
        )

    welcome_text = (
        "السلام عليكم ورحمة الله وبركاته 🌿\n"
        "أهلاً بك في *بوت سراج المؤمن* 💫\n\n"
        "اختر ما تشاء من الأزرار أدناه لتذكِّر قلبك بالله 🤍"
    )

    if update.message is None:
        return
    
    await update.message.reply_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )
    logger.info(f"User: {user_display} has started the bot.")


# ======= Bot Commands =======
async def post_init(application):
    commands = [
        BotCommand("/start", "يدء تشغيل البوت")
    ]
    await application.bot.set_my_commands(commands)

# ======= Handling button presses =======

SYNC_HANDLER = {
    "🌅 أذكار الصباح": morning_adhkar,
    "🌙 أذكار المساء": evening_adhkar,
    "💭 ذكر من الأذكار": general_adhkar,
    "🤲 دعاء من القرآن": get_random_dua,
}

ASYNC_HANDLER = {
    "📖 آية من القرآن": get_random_ayah,
    "📜 حديث شريف": get_random_hadith,
    "✍️ حديث قُدسي": get_random_hadith_qudsi,
}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None or message.text is None:
        return

    user_text = message.text
    try:
        if user_text in SYNC_HANDLER:
            text = SYNC_HANDLER[user_text]()
        elif user_text in ASYNC_HANDLER:
            text = await ASYNC_HANDLER[user_text]()
        else:
            await message.reply_text("⚠️ خيار غير معروف، اختر من الأزرار المتاحة 👇")
            return
        
        await message.reply_text(text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error handling message '{user_text}': {type(e).__name__}: {e}", exc_info=True)
        await message.reply_text("عذراً، تعذر الاتصال الآن، حاول مرة أخرى من فضلك 🙏")

# Start the bot
if __name__ == "__main__":
    print("🚀 Bot is running...")

    app = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(post_init)
        .request(HTTPXRequest(connect_timeout=20, read_timeout=20))
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(allowed_updates=Update.ALL_TYPES)
