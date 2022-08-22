from datetime import datetime

from pyrogram import filters
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    Message)

from RajniiRobot import pgram, OWNER_ID, OWNER_USERNAME, SUPPORT_CHAT
from RajniiRobot.utils.errors import capture_err


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if msg.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return msg.text.split(None, 1)[1]
    except IndexError:
        return None


@pgram.on_message(filters.command("greport"))
@capture_err
async def bug(_, msg: Message):
    if msg.chat.username:
        chat_username = (f"@{msg.chat.username} / `{msg.chat.id}`")
    else:
        chat_username = (f"Private Group / `{msg.chat.id}`")

    bugs = content(msg)
    user_id = msg.from_user.id
    mention = (
        f"[{msg.from_user.first_name}](tg://user?id={str(msg.from_user.id)}"
        + ")"
    )

    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    gban_request = f"""
**#GBAN_REQUEST**
**Appealed by : ** **{mention}**
**Chat : ** **{chat_username}**
**Report Details:** `{bugs}`
**Event Stamp :** `{datetimes}`
"""

    if msg.chat.type == "private":
        await msg.reply_text("❎ <b>This command only works in groups.</b>")
        return

    if user_id == OWNER_ID:
        if bugs:
            await msg.reply_text("❎ <b>Why tf you're appealing a gban request, you're my main dev right?</b>")
            return
        await msg.reply_text("Owner noob!")

    elif bugs:
        await msg.reply_text(
            f"<b>Gban Request :</b> <code>{bugs}</code>\n\n"
            "✅ <b>User has been reported to the Support chat!</b>",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Close", callback_data="grequest_close_reply")]]))

        thumb = "https://bit.ly/3QHKHu5"
        await pgram.send_photo(
            SUPPORT_CHAT,
            photo=thumb,
            caption=f"{gban_request}",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("➡ View Gban Appeal", url=f"{msg.link}")],
                 [InlineKeyboardButton("❌ Close", callback_data="close_gban_request")]]))
    else:
        await msg.reply_text("❎ <b>No Details given to report a user!</b>")


@pgram.on_callback_query(filters.regex("grequest_close_reply"))
async def grequest_close_reply(msg, CallbackQuery):
    await CallbackQuery.message.delete()


@pgram.on_callback_query(filters.regex("close_gban_request"))
async def close_gban_request(_, CallbackQuery):
    is_Admin = await pgram.get_chat_member(CallbackQuery.message.chat.id, CallbackQuery.from_user.id)
    if not is_Admin.can_delete_messages:
        return await CallbackQuery.answer("You're not allowed to close this.", show_alert=True)
    await CallbackQuery.message.delete()

__mod_name__ = "GbanRequest"
