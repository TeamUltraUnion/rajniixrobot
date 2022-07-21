import json
import re
import os
import html
import requests
from RajniiRobot import AI_API_KEY
import RajniiRobot.modules.sql.kuki_sql as sql

from time import sleep
from telegram import ParseMode
from telegram import (CallbackQuery, Chat, MessageEntity, InlineKeyboardButton,
                      InlineKeyboardMarkup, Message, ParseMode, Update, Bot, User)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          DispatcherHandlerStop, Filters, MessageHandler,
                          run_async)
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown

from RajniiRobot.modules.helper_funcs.filters import CustomFilters
from RajniiRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from RajniiRobot import dispatcher, updater, SUPPORT_CHAT
from RajniiRobot.modules.log_channel import gloggable


@user_admin_no_reply
@gloggable
@run_async
def rm_ai(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"rm_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_kuki = sql.rem_kuki(chat.id)
        if is_kuki:
            is_kuki = sql.rem_kuki(user_id)
            return (
                f"<b>{html.escape(chat.title)}:</b>\n"
                f"AI_DEACTIVATED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Rajni AI Chat module Deactivated by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@user_admin_no_reply
@gloggable
@run_async
def add_ai(update: Update, context: CallbackContext) -> str:
    query: Optional[CallbackQuery] = update.callback_query
    user: Optional[User] = update.effective_user
    match = re.match(r"add_chat\((.+?)\)", query.data)
    if match:
        user_id = match.group(1)
        chat: Optional[Chat] = update.effective_chat
        is_kuki = sql.set_kuki(chat.id)
        if is_kuki:
            is_kuki = sql.set_kuki(user_id)
            return (
                f"<b>{html.escape(chat.title)}</b>\n"
                f"AI_ACTIVATED\n"
                f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
            )
        else:
            update.effective_message.edit_text(
                "Rajni AI Chat module Activated by {}.".format(mention_html(user.id, user.first_name)),
                parse_mode=ParseMode.HTML,
            )

    return ""

@user_admin
@gloggable
@run_async
def aichat_toggle(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message
    msg = f"Choose an option below to toggle ai chatbot."
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            text="◇ Activate",
            callback_data="add_chat({})")],
       [
        InlineKeyboardButton(
            text="◇ Deactivate",
            callback_data="rm_chat({})")]])
    message.reply_text(
        msg,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
    )

def get_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "rajni":
        return True
    if reply_message:
        if reply_message.from_user.id == context.bot.get_me().id:
            return True
    else:
        return False

@run_async
def ai_reply(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot
    is_kuki = sql.is_kuki(chat_id)
    if not is_kuki:
        return

    if message.text and not message.document:
        if not get_message(context, message):
            return
        Message = message.text
        bot.send_chat_action(chat_id, action="typing")
        kukiurl = requests.get(f'{AI_API_KEY}'+Message)
        Kuki = json.loads(kukiurl.text)
        kuki = Kuki['reply']
        sleep(0.3)
        message.reply_text(kuki, timeout=60)

@run_async
def ai_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_kuki_chats()
    text = "<b>AI Chatbot-Enabled in these Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title or x.first_name
            text += f"◇ <code>{name}</code>\n"
        except (BadRequest, Unauthorized):
            sql.rem_kuki(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")

__help__ = f"""
AI Chat Module utilizes the Kuki's api which allows {dispatcher.bot.first_name} to talk and provide a more interactive group chat experience.
*Admins only Commands*:
  ◇ `/aichat`*:* Will ask you to on/off AI Chatbot.
*Powered by Itel Ai*
"""

__mod_name__ = "AIChat"


CHATBOTK_HANDLER = CommandHandler("aichat", aichat_toggle)
ADD_CHAT_HANDLER = CallbackQueryHandler(add_ai, pattern=r"add_chat")
RM_CHAT_HANDLER = CallbackQueryHandler(rm_ai, pattern=r"rm_chat")
CHATBOT_HANDLER = MessageHandler(
    Filters.text & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!")
                    & ~Filters.regex(r"^\/")), ai_reply)
LIST_ALL_CHATS_HANDLER = CommandHandler(
    "aichats", ai_chats, filters=CustomFilters.dev_filter)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(LIST_ALL_CHATS_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    LIST_ALL_CHATS_HANDLER,
    CHATBOT_HANDLER,
]