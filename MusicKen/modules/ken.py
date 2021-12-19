from pyrogram import Client

from MusicKen.config import BOT_USERNAME
from MusicKen.helpers.filters import command
from MusicKen.services.callsmusic.callsmusic import client as USER


@Client.on_message(command(["lson", f"lson@{BOT_USERNAME}"]))
async def songs(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "❌ **Song Not found.**\n\n**Try Entering a clearer song title.**"
            )
            return
        text = message.text.split(None, 1)[1]
        results = await USER.get_inline_bot_results(119606003, f"{text}")
        await USER.send_inline_bot_result(
            message.chat.id, results.query_id, results.results[0].id
        )
    except Exception:
        await message.reply_text("❌ **Song Not found..**")
