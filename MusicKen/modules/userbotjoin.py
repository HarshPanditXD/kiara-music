import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from MusicKen.config import SUDO_USERS
from MusicKen.helpers.decorators import authorized_users_only, errors
from MusicKen.services.callsmusic.callsmusic import client as USER


@Client.on_message(filters.command(["userbotjoin"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    message.chat.id
    try:
        invite_link = await client.chat.export_invite_link()
        if "+" in invite_link:
            link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
    except:
        await message.reply_text(
            "<b>Add me as your group admin first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicKen"

    try:
        await USER.join_chat(f"https://t.me/joinchat/{link_hash}")
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} already in your chat</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} can't join your group due to many join requests for userbot! Make sure the user is not banned in the group."
            "\n\nOr add Assistant bot manually to your Group and try again.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} berhasil join your chat</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b>Users cannot leave your group!  Maybe wait floodwaits."
            "\n\nOr manually remove me from your Groups</b>",
        )
        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("**Assistant Leave all chats**")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"Assistant left... It worked: {left} chat.  Failed: {failed} chat."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"Assistant left... Success: {left} chat.  Failed: {failed} chat."
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Successful {left} chat.  Failed {failed} chat."
        )


@Client.on_message(
    filters.command(["userbotjoinchannel", "ubjoinc"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("Is the chat connected?")
        return
    try:
        await client.export_chat_invite_link(chid)
        if "+" in invite_link:
            link_hash = (invite_link.replace("+", "")).split("t.me/")[1]
    except:
        await message.reply_text(
            "<b>Add me as your channel admin first</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "MusicKen"

    try:
        await USER.join_chat(f"https://t.me/joinchat/{link_hash}")
    except UserAlreadyParticipant:
        await message.reply_text(
            f"<b>{user.first_name} already on your channel</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>⛑ Flood Wait Error ⛑\n{user.first_name} can't join your group due to the large number of join requests for userbot!  Make sure the user is not banned in the group."
            "\n\nOr add Assistant bot manually to your Group and try again.</b>",
        )
        return
    await message.reply_text(
        f"<b>{user.first_name} already joined your chat</b>",
    )
