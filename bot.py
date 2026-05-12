import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

def score_die(value):
    if value in [2, 4]:
        return 1
    elif value == 6:
        return 2
    return 0

async def roll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /r 5d6")
        return

    try:
        dice_input = context.args[0].lower()

        if dice_input.endswith("d6"):
            dice_input = dice_input[:-2]

        amount = int(dice_input)

    except:
        await update.message.reply_text("Please use a format like: /r 5d6")
        return

    rolls = [random.randint(1, 6) for _ in range(amount)]
    scores = [score_die(r) for r in rolls]
    total = sum(scores)

    text = (
        f"🎲 Rolled: {', '.join(map(str, rolls))}\n"
        f"⭐ Points: {' + '.join(map(str, scores))} = {total}"
    )

    await update.message.reply_text(text)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("roll", roll))
app.add_handler(CommandHandler("r", roll))

print("Bot running...")
app.run_polling()