import html
import math
import asyncio
import heroku3
import re
import os
import requests

from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import ChannelParticipantsAdmins
from telethon import events
from pyrogram import filters

from RajniiRobot import ARQ_API_URL, pgram as app, arq
from telegram import MAX_MESSAGE_LENGTH, ParseMode, Update, MessageEntity
from telegram.ext import CallbackContext, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.error import BadRequest
from telegram.utils.helpers import escape_markdown, mention_html

from RajniiRobot import (
    DEV_USERS,
    OWNER_ID,
    DRAGONS,
    DEMONS,
    TIGERS,
    WOLVES,
    INFOPIC,
    HEROKU_APP_NAME,
    dispatcher,
    sw,
)
from RajniiRobot import telethn as borg, HEROKU_APP_NAME, HEROKU_API_KEY, OWNER_ID
from RajniiRobot.events import register
from RajniiRobot.__main__ import STATS, TOKEN, USER_INFO
import RajniiRobot.modules.sql.userinfo_sql as sql
from RajniiRobot.modules.disable import DisableAbleCommandHandler
from RajniiRobot.modules.sql.global_bans_sql import is_user_gbanned
from RajniiRobot.modules.sql.afk_sql import is_afk, check_afk_status
from RajniiRobot.modules.sql.users_sql import get_user_num_chats
from RajniiRobot.modules.helper_funcs.chat_status import sudo_plus
from RajniiRobot.modules.helper_funcs.extraction import extract_user
from RajniiRobot import telethn as SaitamaTelethonClient
from RajniiRobot.modules.arq import arq_stats
# from RajniiRobot.modules.heroku.dyno_usage import AppHours, AppMinutes, AppPercentage, hours, minutes, percentage

# ARQ INFO
# ARQ INFO
"""
@app.on_message(filters.command("arq"))
async def arq_stats(_, message):
    data = await arq.stats()
    if not data.ok:
        return await message.reply_text(data.result)
    data = data.result
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    users = data.users
    bot = data.bot
    statistics = f""" """
**Uptime:** `{uptime}`
**Requests Since Uptime:** `{requests}`
**CPU:** `{cpu}`
**Memory:**
    **Total Used:** `{server_mem}`
    **API:** `{api_mem}`
**Disk:** `{disk}`
**Platform:** `{platform}`
**Python:** `{python_version}`
**Users:** `{users}`
**Bot:** {bot}
**Address:** {ARQ_API_URL}"""
"""
    await message.reply_text(
        statistics, disable_web_page_preview=True)

"""

# HEROKU
# HEROKU

heroku_api = "https://api.heroku.com"
Heroku = heroku3.from_key(HEROKU_API_KEY)


@register(pattern=r"^/(set|see|del) var(?: |$)(.*)(?: |$)([\s\S]*)")
async def variable(var):
    if var.fwd_from:
        return
    if var.sender_id == OWNER_ID:
        pass
    else:
        return
    """
    Manage most of ConfigVars setting, set new var, get current var,
    or delete var...
    """
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        return await var.reply("`[HEROKU]:"
                               "\nPlease setup your` **HEROKU_APP_NAME**")
    exe = var.pattern_match.group(1)
    heroku_var = app.config()
    if exe == "see":
        k = await var.reply("`Getting information...`")
        await asyncio.sleep(1.5)
        try:
            variable = var.pattern_match.group(2).split()[0]
            if variable in heroku_var:
                return await k.edit(
                    "**ConfigVars**:"
                    f"\n\n`{variable} = {heroku_var[variable]}`\n")
            return await k.edit("**ConfigVars**:"
                                f"\n\n`Error:\n-> {variable} don't exists`")
        except IndexError:
            configs = prettyjson(heroku_var.to_dict(), indent=2)
            with open("configs.json", "w") as fp:
                fp.write(configs)
            with open("configs.json", "r") as fp:
                result = fp.read()
                if len(result) >= 4096:
                    await var.client.send_file(
                        var.chat_id,
                        "configs.json",
                        reply_to=var.id,
                        caption="`Output too large, sending it as a file`",
                    )
                else:
                    await k.edit("`[HEROKU]` ConfigVars:\n\n"
                                 "================================"
                                 f"\n```{result}```\n"
                                 "================================")
            os.remove("configs.json")
            return
    elif exe == "set":
        s = await var.reply("`Setting information...weit ser`")
        variable = var.pattern_match.group(2)
        if not variable:
            return await s.edit(">`.set var <ConfigVars-name> <value>`")
        value = var.pattern_match.group(3)
        if not value:
            variable = variable.split()[0]
            try:
                value = var.pattern_match.group(2).split()[1]
            except IndexError:
                return await s.edit(">`/set var <ConfigVars-name> <value>`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await s.edit(
                f"**{variable}**  `successfully changed to`  ->  **{value}**")
        else:
            await s.edit(
                f"**{variable}**  `successfully added with value`  ->  **{value}**"
            )
        heroku_var[variable] = value
    elif exe == "del":
        m = await var.edit("`Getting information to deleting variable...`")
        try:
            variable = var.pattern_match.group(2).split()[0]
        except IndexError:
            return await m.edit(
                "`Please specify ConfigVars you want to delete`")
        await asyncio.sleep(1.5)
        if variable in heroku_var:
            await m.edit(f"**{variable}**  `successfully deleted`")
            del heroku_var[variable]
        else:
            return await m.edit(f"**{variable}**  `is not exists`")


@register(pattern="^/usage(?: |$)")
async def dyno_usage(dyno):
    if dyno.fwd_from:
        return
    if dyno.sender_id == OWNER_ID:
        pass
    else:
        return
    """
    Get your account Dyno Usage
    """
    die = await dyno.reply("**Processing...**")
    useragent = ("Mozilla/5.0 (Linux; Android 10; SM-G975F) "
                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                 "Chrome/80.0.3987.149 Mobile Safari/537.36")
    user_id = Heroku.account().id
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + user_id + "/actions/get-quota"
    r = requests.get(heroku_api + path, headers=headers)
    if r.status_code != 200:
        return await die.edit("`Error: something bad happened`\n\n"
                              f">.`{r.reason}`\n")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    """ - Used - """
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    """ - Current - """
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)

    await asyncio.sleep(1.5)

    return await die.edit("**Dyno Usage**:\n\n"
                          f" -> `Dyno usage for`  **{HEROKU_APP_NAME}**:\n"
                          f"     ❍  `{AppHours}`**h**  `{AppMinutes}`**m**  "
                          f"**|**  [`{AppPercentage}`**%**]"
                          "\n\n"
                          " -> `Dyno hours quota remaining this month`:\n"
                          f"     ❍  `{hours}`**h**  `{minutes}`**m**  "
                          f"**|**  [`{percentage}`**%**]")


def prettyjson(obj, indent=2, maxlinelength=80):
    """Renders JSON content with indentation and line splits/concatenations to fit maxlinelength.
    Only dicts, lists and basic types are supported"""

    items, _ = getsubitems(
        obj,
        itemkey="",
        islast=True,
        maxlinelength=maxlinelength - indent,
        indent=indent,
    )
    return indentitems(items, indent, level=0)


# HEROKU
# HEROKU


def no_by_per(totalhp, percentage):
    """
    rtype: num of `percentage` from total
    eg: 1000, 10 -> 10% of 1000 (100)
    """
    return totalhp * percentage / 100


def get_percentage(totalhp, earnedhp):
    """
    rtype: percentage of `totalhp` num
    eg: (1000, 100) will return 10%
    """

    matched_less = totalhp - earnedhp
    per_of_totalhp = 100 - matched_less * 100.0 / totalhp
    per_of_totalhp = str(int(per_of_totalhp))
    return per_of_totalhp


def hpmanager(user):
    total_hp = (get_user_num_chats(user.id) + 10) * 10

    if not is_user_gbanned(user.id):

        # Assign new var `new_hp` since we need `total_hp` in
        # end to calculate percentage.
        new_hp = total_hp

        # if no username decrease 25% of hp.
        if not user.username:
            new_hp -= no_by_per(total_hp, 25)
        try:
            dispatcher.bot.get_user_profile_photos(user.id).photos[0][-1]
        except IndexError:
            # no profile photo ==> -25% of hp
            new_hp -= no_by_per(total_hp, 25)
        # if no /setme exist ==> -20% of hp
        if not sql.get_user_me_info(user.id):
            new_hp -= no_by_per(total_hp, 20)
        # if no bio exsit ==> -10% of hp
        if not sql.get_user_bio(user.id):
            new_hp -= no_by_per(total_hp, 10)

        if is_afk(user.id):
            afkst = check_afk_status(user.id)
            # if user is afk and no reason then decrease 7%
            # else if reason exist decrease 5%
            if not afkst.reason:
                new_hp -= no_by_per(total_hp, 7)
            else:
                new_hp -= no_by_per(total_hp, 5)

        # fbanned users will have (2*number of fbans) less from max HP
        # Example: if HP is 100 but user has 5 diff fbans
        # Available HP is (2*5) = 10% less than Max HP
        # So.. 10% of 100HP = 90HP

    # Commenting out fban health decrease cause it wasnt working and isnt needed ig.
    # _, fbanlist = get_user_fbanlist(user.id)
    # new_hp -= no_by_per(total_hp, 2 * len(fbanlist))

    # Bad status effects:
    # gbanned users will always have 5% HP from max HP
    # Example: If HP is 100 but gbanned
    # Available HP is 5% of 100 = 5HP

    else:
        new_hp = no_by_per(total_hp, 5)

    return {
        "earnedhp": int(new_hp),
        "totalhp": int(total_hp),
        "percentage": get_percentage(total_hp, new_hp),
    }


def make_bar(per):
    done = min(round(per / 10), 10)
    return "■" * done + "□" * (10 - done)


@run_async
def get_id(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    msg = update.effective_message
    user_id = extract_user(msg, args)

    if user_id:

        if msg.reply_to_message and msg.reply_to_message.forward_from:

            user1 = message.reply_to_message.from_user
            user2 = message.reply_to_message.forward_from

            msg.reply_text(
                f"<b>Telegram ID:</b>\n"
                f"<b>◇ {html.escape(user1.first_name)} -</b> <code>{user1.id}</code>.\n"
                f"<b>◇ {html.escape(user2.first_name)} -</b> <code>{user2.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:

            user = bot.get_chat(user_id)
            msg.reply_text(
                f"{html.escape(user.first_name)}'s id is <code>{user.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

    else:

        if chat.type == "private":
            msg.reply_text(
                f"Your id is <code>{chat.id}</code>.",
                parse_mode=ParseMode.HTML,
            )

        else:
            msg.reply_text(
                # f"Your ID is <code>{user1.id}</code>"
                f"This group's id is <code>{chat.id}</code>.",
                parse_mode=ParseMode.HTML,
            )


@SaitamaTelethonClient.on(
    events.NewMessage(
        pattern="/ginfo ",
        from_users=(TIGERS or []) + (DRAGONS or []) + (DEMONS or []),
    ), )
async def group_info(event) -> None:
    chat = event.text.split(" ", 1)[1]
    try:
        entity = await event.client.get_entity(chat)
        totallist = await event.client.get_participants(
            entity,
            filter=ChannelParticipantsAdmins,
        )
        ch_full = await event.client(GetFullChannelRequest(channel=entity))
    except:
        await event.reply(
            "Can't for some reason, maybe it is a private one or that I am banned there.",
        )
        return
    msg = f"**ID**: `-100{entity.id}`"
    msg += f"\n**Title**: `{entity.title}`"
    msg += f"\n**Datacenter**: `{entity.photo.dc_id}`"
    msg += f"\n**Video PFP**: `{entity.photo.has_video}`"
    msg += f"\n**Supergroup**: `{entity.megagroup}`"
    msg += f"\n**Restricted**: `{entity.restricted}`"
    msg += f"\n**Scam**: `{entity.scam}`"
    msg += f"\n**Slowmode**: `{entity.slowmode_enabled}`"
    if entity.username:
        msg += f"\n**Username**: @{entity.username}"
    msg += "\n\n**Member Stats:**"
    msg += f"\n`Admins:` `{len(totallist)}`"
    msg += f"\n`Users`: `{totallist.total}`"
    msg += "\n\n**Admins List:**"
    for x in totallist:
        msg += f"\n◇ [{x.id}](tg://user?id={x.id})"
    msg += f"\n\n**Description**:\n`{ch_full.full_chat.about}`"
    await event.reply(msg)


@run_async
def gifid(update: Update, context: CallbackContext):
    msg = update.effective_message
    if msg.reply_to_message and msg.reply_to_message.animation:
        update.effective_message.reply_text(
            f"Gif ID:\n<code>{msg.reply_to_message.animation.file_id}</code>",
            parse_mode=ParseMode.HTML,
        )
    else:
        update.effective_message.reply_text(
            "Please reply to a gif to get its ID.")


@run_async
def info(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (
            not args or
        (len(args) >= 1 and not args[0].startswith("@")
         and not args[0].isdigit()
         and not message.parse_entities([MessageEntity.TEXT_MENTION]))):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return

    rep = message.reply_text("<code>Appraising...</code>",
                             parse_mode=ParseMode.HTML)

    text = (f"╒═══「<b> User info </b>」\n"
            f"<b>User ID:</b> <code>{user.id}</code>\n"
            f"<b>First Name:</b> {html.escape(user.first_name)}")

    if user.last_name:
        text += f"\n<b>Last Name:</b> {html.escape(user.last_name)}"

    if user.username:
        text += f"\n<b>Username:</b> @{html.escape(user.username)}"

    text += f"\n<b>User link:</b> {mention_html(user.id, 'link')}"

    if chat.type != "private" and user_id != bot.id:
        _stext = "\n<b>Presence:</b> <code>{}</code>"

        afk_st = is_afk(user.id)
        if afk_st:
            text += _stext.format("AFK")
        else:
            status = status = bot.get_chat_member(chat.id, user.id).status
            if status:
                if status in {"left", "kicked"}:
                    text += _stext.format("Not in this chat")
                elif status == "member":
                    text += _stext.format("Detected")
                elif status in {"administrator", "creator"}:
                    text += _stext.format("Admin")
    if user_id not in [bot.id, 777000, 1087968824]:
        userhp = hpmanager(user)
        text += f"\n\n<b>Health:</b> <code>{userhp['earnedhp']}/{userhp['totalhp']}</code>\n[<i>{make_bar(int(userhp['percentage']))}</i> {userhp['percentage']}%]"

    try:
        spamwtc = sw.get_ban(int(user.id))
        if spamwtc:
            text += f"\n\nThis person is Spamwatched!"
            text += f"\nReason:</b> <pre>{spamwtc.reason}</pre>"
            text += f"\nAppeal bans at @SpamWatchSupport"
        else:
            pass
    except:
        pass  # don't crash if api is down somehow...

    disaster_level_present = False

    if user.id == OWNER_ID:
        text += "\n\nThis User is my main developer."
        disaster_level_present = True
    elif user.id in DEV_USERS:
        text += "\n\nThis User is one of our Association’s developers."
        disaster_level_present = True
    elif user.id in DRAGONS:
        text += "\n\nThis person is one of my SUDO or a DRAGON users, stay alert from them."
        disaster_level_present = True
    elif user.id in DEMONS:
        text += "\n\nThis person is from our SUPPORT staff or a DEMON users."
        disaster_level_present = True
    elif user.id in TIGERS:
        text += "\n\nThis person is one of my TIGER users."
        disaster_level_present = True
    elif user.id in WOLVES:
        text += "\n\nThis person is one of my WHITELISTED or WOLF users"
        disaster_level_present = True

    if disaster_level_present:
        text += ' [<a href="https://t.me/RajniUpdates/93">?</a>]'

    try:
        user_member = chat.get_member(user.id)
        if user_member.status == "administrator":
            result = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}",
            )
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result["custom_title"]
                text += f"\n\n<b>Title:</b> <code>{custom_title}</code>"
    except BadRequest:
        pass

    for mod in USER_INFO:
        try:
            mod_info = mod.__user_info__(user.id).strip()
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    if INFOPIC:
        try:
            profile = context.bot.get_user_profile_photos(
                user.id).photos[0][-1]
            _file = bot.get_file(profile["file_id"])
            _file.download(f"{user.id}.png")

            message.reply_document(
                document=open(f"{user.id}.png", "rb"),
                caption=(text),
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )

            os.remove(f"{user.id}.png")
        # Incase user don't have profile pic, send normal text
        except IndexError:
            message.reply_text(
                text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False,
            )

    else:
        message.reply_text(
            text,
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=False,
        )

    rep.delete()


@run_async
def about_me(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    user_id = extract_user(message, args)

    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_me_info(user.id)

    if info:
        update.effective_message.reply_text(
            f"*{user.first_name}*:\n{escape_markdown(info)}",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = message.reply_to_message.from_user.first_name
        update.effective_message.reply_text(
            f"{username} hasn't set an info message about themselves yet!", )
    else:
        update.effective_message.reply_text(
            "There isnt one, use /setme to set one.")


@run_async
def set_about_me(update: Update, context: CallbackContext):
    message = update.effective_message
    user_id = message.from_user.id
    if user_id in [777000, 1087968824]:
        message.reply_text("Error! Unauthorized")
        return
    bot = context.bot
    if message.reply_to_message:
        repl_message = message.reply_to_message
        repl_user_id = repl_message.from_user.id
        if repl_user_id in [bot.id, 777000, 1087968824] and (user_id
                                                             in DEV_USERS):
            user_id = repl_user_id
    text = message.text
    info = text.split(None, 1)
    if len(info) == 2:
        if len(info[1]) < MAX_MESSAGE_LENGTH // 4:
            sql.set_user_me_info(user_id, info[1])
            if user_id in [777000, 1087968824]:
                message.reply_text("Authorized...Information updated!")
            elif user_id == bot.id:
                message.reply_text(
                    "I have updated my info with the one you provided!")
            else:
                message.reply_text("Information updated!")
        else:
            message.reply_text(
                "The info needs to be under {} characters! You have {}.".
                format(
                    MAX_MESSAGE_LENGTH // 4,
                    len(info[1]),
                ), )


"""
    data = await arq.stats()
    data = data.result
    uptime = data.uptime
    requests = data.requests
    cpu = data.cpu
    server_mem = data.memory.server
    api_mem = data.memory.api
    disk = data.disk
    platform = data.platform
    python_version = data.python
    users = data.users
    bot = data.bot



<b>Uptime:</b> <code>{uptime}</code>
<b>Requests Since Uptime:</b> <code>{requests}</code>
<b>CPU:</b> <code>{cpu}</code>
<b>Memory:</b>
    <b>Total Used:</b> <code>{server_mem}</code>
    <b>API:</b> <code>{api_mem}</code>
<b>Disk:</b> <code>{disk}</code>
<b>Platform:</b> <code>{platform}</code>
<b>Python:</b> <code>{python_version}</code>
<b>Users:</b> <code>{users}</code>
<b>Bot:</b> {bot}
<b>Address:<b> {ARQ_API_URL}


╒═══「 <b>Server statistics</b> 」
<b>Dyno usage for<b> <code>{HEROKU_APP_NAME}<code>
    | <code>{AppHours}</code> <b>hours</b> <code>{AppMinutes}</code> <b>minutes</b>
    | <code>{AppPercentage}%</code>
<b>Dyno hours quota remaining this month:\n</b>
    | <code>{hours}</code> <b>hours</b> <code>{minutes}</code> <b>minutes</b>
    | <code>{percentage}%</code>
"""


@run_async
@sudo_plus
def nstats(update: Update, context: CallbackContext):  #  (_, message)
    stats = f"""
╒═══「 <b>System statistics</b> 」


       <b>「 ARQ stats 」</b>
<b>PTB version:</b> <code>12.8</code>
<b>Python version:</b> <code>3.8.5</code>
<b>Library version:</b> <code>12.8</code>
<b>SRC:</b> <code>Not Available</code>

╒═══「 <b>Rajnii statistics</b> 」
       """ + "\n".join([mod.__stats__() for mod in STATS])
    result = re.sub(r"(\d+)", r"<code>\1</code>", stats)
    update.effective_message.reply_text(result + """

<a href="https://t.me/RajniSupport">✦ Support</a> | <a href="https://t.me/RajniUpdates">✦ Updates</a>
╘══「 <b>By <a href="https://github.com/itzzzzyashu">itzzzyashu</a></b> 」""",
                                        parse_mode=ParseMode.HTML)


@run_async
def about_bio(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message

    user_id = extract_user(message, args)
    if user_id:
        user = bot.get_chat(user_id)
    else:
        user = message.from_user

    info = sql.get_user_bio(user.id)

    if info:
        update.effective_message.reply_text(
            "*{}*:\n{}".format(user.first_name, escape_markdown(info)),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    elif message.reply_to_message:
        username = user.first_name
        update.effective_message.reply_text(
            f"{username} hasn't had a message set about themselves yet!\nSet one using /setbio",
        )
    else:
        update.effective_message.reply_text(
            "You haven't had a bio set about yourself yet!", )


@run_async
def set_about_bio(update: Update, context: CallbackContext):
    message = update.effective_message
    sender_id = update.effective_user.id
    bot = context.bot

    if message.reply_to_message:
        repl_message = message.reply_to_message
        user_id = repl_message.from_user.id

        if user_id == message.from_user.id:
            message.reply_text(
                "Ha, you can't set your own bio! You're at the mercy of others here...",
            )
            return

        if user_id in [777000, 1087968824] and sender_id not in DEV_USERS:
            message.reply_text("You are not authorised")
            return

        if user_id == bot.id and sender_id not in DEV_USERS:
            message.reply_text(
                "Erm... yeah, I only trust Heroes Association to set my bio.",
            )
            return

        text = message.text
        bio = text.split(
            None,
            1,
        )  # use python's maxsplit to only remove the cmd, hence keeping newlines.

        if len(bio) == 2:
            if len(bio[1]) < MAX_MESSAGE_LENGTH // 4:
                sql.set_user_bio(user_id, bio[1])
                message.reply_text(
                    "Updated {}'s bio!".format(
                        repl_message.from_user.first_name), )
            else:
                message.reply_text(
                    "Bio needs to be under {} characters! You tried to set {}."
                    .format(
                        MAX_MESSAGE_LENGTH // 4,
                        len(bio[1]),
                    ), )
    else:
        message.reply_text("Reply to someone to set their bio!")


def __user_info__(user_id):
    bio = html.escape(sql.get_user_bio(user_id) or "")
    me = html.escape(sql.get_user_me_info(user_id) or "")
    result = ""
    if me:
        result += f"<b>About user:</b>\n{me}\n"
    if bio:
        result += f"<b>What others say:</b>\n{bio}\n"
    result = result.strip("\n")
    return result


__help__ = """
*ID:*
 ◇ `/id`*:* get the current group id. If used by replying to a message, gets that user's id.
 ◇ `/gifid`*:* reply to a gif to me to tell you its file ID.
*Self addded information:*
 ◇ `/setme <text>`*:* will set your info
 ◇ `/me`*:* will get your or another user's info.
Examples:
 `/setme I am a wolf.`
 `/me @username(defaults to yours if no user specified)`
*Information others add on you:*
 ◇ `/bio`*:* will get your or another user's bio. This cannot be set by yourself.
◇ `/setbio <text>`*:* while replying, will save another user's bio
Examples:
 `/bio @username(defaults to yours if not specified).`
 `/setbio This user is a wolf` (reply to the user)
*Overall Information about user:*
 ◇ `/info`*:* get information about a user.
*What is that health thingy?*
 Come and see [HP System explained](https://t.me/OnePunchUpdates/192)
"""

SET_BIO_HANDLER = DisableAbleCommandHandler("setbio", set_about_bio)
GET_BIO_HANDLER = DisableAbleCommandHandler("bio", about_bio)

STATS_HANDLER = CommandHandler("nstats", nstats)
ID_HANDLER = DisableAbleCommandHandler("id", get_id)
GIFID_HANDLER = DisableAbleCommandHandler("gifid", gifid)
INFO_HANDLER = DisableAbleCommandHandler(("info", "book"), info)

SET_ABOUT_HANDLER = DisableAbleCommandHandler("setme", set_about_me)
GET_ABOUT_HANDLER = DisableAbleCommandHandler("me", about_me)

dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(GIFID_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(SET_BIO_HANDLER)
dispatcher.add_handler(GET_BIO_HANDLER)
dispatcher.add_handler(SET_ABOUT_HANDLER)
dispatcher.add_handler(GET_ABOUT_HANDLER)

__mod_name__ = "Info"
__command_list__ = ["setbio", "bio", "setme", "me", "info"]
__handlers__ = [
    ID_HANDLER,
    GIFID_HANDLER,
    INFO_HANDLER,
    SET_BIO_HANDLER,
    GET_BIO_HANDLER,
    SET_ABOUT_HANDLER,
    GET_ABOUT_HANDLER,
    STATS_HANDLER,
]
