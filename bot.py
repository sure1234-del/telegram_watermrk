from pyrogram import Client, filters
from config import *
from database import *
from video_processor import process_video
from queue_manager import video_queue, worker
import asyncio
import os

app = Client(
    "watermark_bot",
    api_id=36014101,
    api_hash=d4b9c4246a4a0d16e960677725e8ed8e,
    bot_token="8715679380:AAEqVan2Zd4Carx2ILLs01AxTEb56rfqIKI"
)

user_settings = {}

# START
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Send video to add watermark")

# SETTINGS COMMAND
@app.on_message(filters.command("set"))
async def set_settings(client, message):
    user_id = message.from_user.id

    if not is_premium(user_id):
        return await message.reply("❌ Premium required")

    try:
        _, text, position, speed, opacity = message.text.split(" ")

        user_settings[user_id] = {
            "text": text,
            "position": position,
            "speed": int(speed),
            "opacity": float(opacity)
        }

        await message.reply("✅ Settings updated")

    except:
        await message.reply(
            "Usage:\n/set TEXT position(top/middle/bottom) speed opacity\nExample:\n/set KING top 200 0.8"
        )

# ADMIN COMMANDS
@app.on_message(filters.command("addpremium") & filters.user(OWNER_ID))
async def add_premium_cmd(client, message):
    user_id = int(message.command[1])
    add_premium(user_id)
    await message.reply("User added to premium")

@app.on_message(filters.command("ban") & filters.user(OWNER_ID))
async def ban_cmd(client, message):
    user_id = int(message.command[1])
    ban_user(user_id)
    await message.reply("User banned")

# VIDEO HANDLER
@app.on_message(filters.video)
async def handle_video(client, message):

    user_id = message.from_user.id

    if is_banned(user_id):
        return await message.reply("❌ You are banned")

    await message.reply("⏳ Processing...")

    file_path = await message.download()
    output_path = f"wm_{file_path}"

    settings = user_settings.get(user_id, {
        "text": None,
        "position": "bottom",
        "speed": 150,
        "opacity": 0.7
    })

    await video_queue.put((
        process_and_send,
        (client, message, file_path, output_path, settings)
    ))

# PROCESS FUNCTION
async def process_and_send(client, message, input_path, output_path, settings):

    process_video(
        input_path,
        output_path,
        FORCED_WATERMARK,
        user_text=settings["text"],
        position=settings["position"],
        speed=settings["speed"],
        opacity=settings["opacity"]
    )

    await message.reply_video(
        video=output_path,
        caption="✅ Done"
    )

    # AUTO UPLOAD
    await client.send_video(
        chat_id=CHANNEL_ID,
        video=output_path
    )

    os.remove(input_path)
    os.remove(output_path)
    
from pyrogram import idle
import asyncio

# START QUEUE WORKER

async def main():
    asyncio.create_task(worker())
    await app.start()
    print("Bot Running...")
    await idle()

if name == "main":
    asyncio.run(main())
