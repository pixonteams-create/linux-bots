import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("9026868145:AAESqFmEGX0ze-p8yzRw6UnldsyL3UO2Ipg")
HF_TOKEN = os.environ.get("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")
MODEL = "runwayml/stable-diffusion-v1-5"

def make_image(prompt):
    url = f"https://api-inference.huggingface.co/models/{MODEL}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    r = requests.post(url, headers=headers, json={"inputs": prompt})
    return r.content

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Prompt bhejo - jaise 'a cute boy in Delhi'")

async def gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text
    await update.message.reply_text(f"Ban raha hai: {prompt} 🎨 30 sec...")
    try:
        img = make_image(prompt)
        if len(img) < 2000:
            await update.message.reply_text("Model load ho raha hai, 1 min baad fir try karo!")
        else:
            await update.message.reply_photo(photo=img, caption=prompt)
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, gen))
print("Bot is Live 24x7")
app.run_polling()
