import pyrogram
import os
import asyncio
import re

try:
    app_id = int(os.environ.get("app_id", None))
except Exception as app_id:
    print(f"⚠️ App ID Invalid {app_id}")
try:
    api_hash = os.environ.get("api_hash", None)
except Exception as api_id:
    print(f"⚠️ Api Hash Invalid {api_hash}")
try:
    bot_token = os.environ.get("bot_token", None)
except Exception as bot_token:
    print(f"⚠️ Bot Token Invalid {bot_token}")
try:
    custom_caption = os.environ.get("custom_caption", "")
except Exception as custom_caption:
    print(f"⚠️ Custom Caption Invalid {custom_caption}")

AutoCaptionBotV1 = pyrogram.Client(
    name="AutoCaptionBotV1", api_id=app_id, api_hash=api_hash, bot_token=bot_token)

start_message = """
<b>👋Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power</b>
<b>@kwicbotupdates</b>"""

about_message = """
<b>• Name : <a href=https://t.me/kwic2002>kwic autocaption</a></b>
<b>• Developer : <a href=https://t.me/kwicbotupdates>[KWICBOT UPDATES]</a></b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href=https://t.me/kwicbotupdates>Click Here</a></b>
<b>• Source Code : <a href=https://github.com/PR0-99/CaptionBot-V1>Click Here</a></b>"""

@AutoCaptionBotV1.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(start_message.format(update.from_user.mention), reply_markup=start_buttons(bot, update),
                  parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("start"))
def strat_callback(bot, update):
    update.message.edit(start_message.format(update.from_user.mention), reply_markup=start_buttons(bot, update.message),
                         parse_mode=pyrogram.enums.ParseMode.HTML, disable_web_page_preview=True)

@AutoCaptionBotV1.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(about_message.format(version=pyrogram.__version__, username=bot.mention),
                        reply_markup=about_buttons(bot, update.message), parse_mode=pyrogram.enums.ParseMode.HTML,
                        disable_web_page_preview=True)

@AutoCaptionBotV1.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    try:
        old_caption = update.caption
        if old_caption:
            # Replace other usernames with '@MS_Update_Channel'
            old_caption_with_ms_update_channel = replace_usernames_with_ms_update_channel(old_caption)
            new_caption = f"{old_caption_with_ms_update_channel}\n\n<b>〽️ Join @MS_Update_Channel</b>"
            update.edit(new_caption, parse_mode="html")
    except pyrogram.errors.MessageNotModified:
        pass

def replace_usernames_with_ms_update_channel(caption):
    # Define a regular expression pattern for detecting usernames in captions
    username_pattern = re.compile(r'@[\w_]+')

    # Use the sub function to replace usernames with '@MS_Update_Channel'
    clean_caption = re.sub(username_pattern, '@MS_Update_Channel', caption)

    return clean_caption

def start_buttons(bot, update):
    bot = bot.get_me()
    buttons = [[
        pyrogram.types.InlineKeyboardButton("Updates", url="t.me/kwicbotupdates"),
        pyrogram.types.InlineKeyboardButton("About 🤠", callback_data="about")
    ], [
        pyrogram.types.InlineKeyboardButton("➕️ Add To Your Channel ➕️", url=f"http://t.me/{bot.username}?startchannel=true")
    ]]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
    buttons = [[
        pyrogram.types.InlineKeyboardButton("🏠 Back To Home 🏠", callback_data="start")
    ]]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

print("Telegram AutoCaption V1 Bot Start")
print("Bot Created By https://t.me/kwicbotupdates")

AutoCaptionBotV1.run()
