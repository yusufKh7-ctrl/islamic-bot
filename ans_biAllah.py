
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

import random
from adhkar_data import *


# ======= /start =======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📖 آية من القرآن", callback_data="ayah")],
        [InlineKeyboardButton("🕊️ حديث شريف", callback_data="hadith")],
        [InlineKeyboardButton("💭 ذكر من الأذكار", callback_data="dhikr")],
        [InlineKeyboardButton("🙏 دعاء من القرآن", callback_data="quran_dua")],
        [InlineKeyboardButton("🌅 أذكار الصباح", callback_data="morning")],
        [InlineKeyboardButton("🌙 أذكار المساء", callback_data="evening")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "السلام عليكم ورحمة الله وبركاته 🌿\n"
        "أهلاً بك في *بوت سراج المؤمن* 💫\n\n"
        "اختر ما تشاء من الأزرار أدناه لتذكِّر قلبك بالله 🤍"
    )

    await update.message.reply_text(
        welcome_text, reply_markup=reply_markup, parse_mode="Markdown"
    )


# ======= التعامل مع الضغط على الأزرار =======
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    try:
        await query.answer()  # لازم بسرعة حتى ما يعطي timeout

        # تحديد نوع الزر
        data_map = {
            "ayah": ("📖 آية من القرآن:\n\n", ayat),
            "hadith": ("🕊️ حديث شريف:\n\n", ahadith),
            "dhikr": ("💭 ذكر من الأذكار:\n\n", adhkar),
            "quran_dua": ("🙏 دعاء من القرآن:\n\n", quran_duas),
            "morning": ("🌅 *أذكار الصباح:*\n\n", morning_adhkar),
            "evening": ("🌙 *أذكار المساء:*\n\n", evening_adhkar),
        }

        if query.data in data_map:
            title, content = data_map[query.data]
            if isinstance(content, list):
                if query.data in ["morning", "evening"]:
                    text = title + "\n\n".join(content)
                    await query.message.reply_text(text, parse_mode="Markdown")
                else:
                    text = title + random.choice(content)
                    await query.message.reply_text(text, parse_mode="Markdown")
            else:
                await query.message.reply_text("⚠️ حدث خطأ في تحميل البيانات.")

        else:
            await query.message.reply_text("⚠️ خيار غير معروف.")

    except Exception as e:
        # هذا الجزء يمنع الكود من الانهيار ويطبع المشكلة فقط
        print(f"⚠️ Error: {e}")


# ======= تشغيل البوت =======
if __name__ == "__main__":
    print("🚀 Bot is running...")

    app = (
        ApplicationBuilder()
        .token("8331151810:AAHeCEpxqfbCsXVLA5H2Jayatu1G7_An_o0")
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling(allowed_updates=Update.ALL_TYPES)
