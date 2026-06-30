from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = "8568839659:AAF2B_K5-29trZYRacIiElKX9kZvuqwybio"
ADMIN_ID = 5461253291  # آیدی عددی مدیر

saved_message = None
waiting_for_message = False

CHANNEL = "@v2ray0config"
GROUP = "@G_v2ray0config"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saved_message

    user_id = update.effective_user.id

    try:
        ch = await context.bot.get_chat_member(CHANNEL, user_id)
        gp = await context.bot.get_chat_member(GROUP, user_id)

        if ch.status in ["member", "administrator", "creator"] and \
           gp.status in ["member", "administrator", "creator"]:

            if saved_message:
                await update.message.reply_text(saved_message)
            else:
                await update.message.reply_text("هنوز پیامی تنظیم نشده است.")

        else:
            await update.message.reply_text(
                f"ابتدا در {CHANNEL} و {GROUP} عضو شوید.\n"
                "سپس دوباره /start را ارسال کنید."
            )

    except:
        await update.message.reply_text(
            f"ابتدا در {CHANNEL} و {GROUP} عضو شوید.\n"
            "سپس دوباره /start را ارسال کنید."
        )


async def setmsg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for_message

    if update.effective_user.id != ADMIN_ID:
        return

    waiting_for_message = True
    await update.message.reply_text("پیام موردنظر را ارسال کنید.")


async def save_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global saved_message, waiting_for_message

    if update.effective_user.id != ADMIN_ID:
        return

    if waiting_for_message:
        saved_message = update.message.text
        waiting_for_message = False
        await update.message.reply_text("پیام ذخیره شد ✅")


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("setmsg", setmsg))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_message))

app.run_polling()