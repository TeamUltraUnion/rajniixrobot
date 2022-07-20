from pyrogram import filters

from RajniiRobot import pgram as app, BOT_USERNAME
from RajniiRobot.utils.errors import capture_err
from RajniiRobot.utils.http import get
from RajniiRobot import SUPPORT_CHAT

@app.on_message(filters.command("repo", f"repo@{BOT_USERNAME}") & ~filters.edited)
@capture_err
async def repo(_, message):
    users = await get(
        "https://api.github.com/repos/TeamSanatanRakshaNetwork/RajniiRoboActive/contributors"
    )
    list_of_users = ""
    count = 1
    for user in users:
        list_of_users += (
            f"**{count}.** [{user['login']}]({user['html_url']})\n"
        )
        count += 1

    text = f"""[Updates](https://t.me/RajniUpdates) | [Support](https://telegram.me/SUPPORT_CHAT)
```
----------------
| Contributors |
----------------
```
{list_of_users}"""
    await app.send_message(
        message.chat.id, text=text, disable_web_page_preview=True)

__mod_name__ = "Devs-Repo"
