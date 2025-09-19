from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from RessoMusic import app
from RessoMusic.utils.database import add_served_chat
from config import LOG_GROUP_ID


async def new_message(chat_id: int, message: str, reply_markup=None):
    """Helper function to send message safely."""
    await app.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)


@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    for user in message.new_chat_members:
        if user.id == bot_id:
            added_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
            title = message.chat.title or "No Title"
            username = f"@{message.chat.username}" if message.chat.username else "No Username"
            chat_id = message.chat.id
            chat_members = await client.get_chat_members_count(chat_id)

            am = (
                f"✫ <b><u>ɴᴇᴡ ɢʀᴏᴜᴘ</u></b> :\n\n"
                f"ᴄʜᴀᴛ ɪᴅ : <code>{chat_id}</code>\n"
                f"ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ : {username}\n"
                f"ᴄʜᴀᴛ ᴛɪᴛʟᴇ : {title}\n"
                f"ᴛᴏᴛᴀʟ ᴄʜᴀᴛ ᴍᴇᴍʙᴇʀꜱ : {chat_members}\n\n"
                f"ᴀᴅᴅᴇᴅ ʙʏ : {added_by}"
            )

            reply_markup = InlineKeyboardMarkup(
                [[InlineKeyboardButton(added_by, user_id=message.from_user.id)]] if message.from_user else []
            )

            await add_served_chat(chat_id)
            await new_message(LOG_GROUP_ID, am, reply_markup)


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    bot_id = (await client.get_me()).id
    if message.left_chat_member and message.left_chat_member.id == bot_id:
        remove_by = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        title = message.chat.title or "No Title"
        username = f"@{message.chat.username}" if message.chat.username else "No Username"
        chat_id = message.chat.id

        ambye = (
            f"✫ <b><u>ʟᴇғᴛ ɢʀᴏᴜᴘ</u></b> :\n\n"
            f"ᴄʜᴀᴛ ɪᴅ : <code>{chat_id}</code>\n"
            f"ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ : {username}\n"
            f"ᴄʜᴀᴛ ᴛɪᴛʟᴇ : {title}\n\n"
            f"ʀᴇᴍᴏᴠᴇᴅ ʙʏ : {remove_by}"
        )

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton(remove_by, user_id=message.from_user.id)]] if message.from_user else []
        )

        await new_message(LOG_GROUP_ID, ambye, reply_markup)