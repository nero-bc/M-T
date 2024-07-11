import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

from bot import Bot
from config import ADMINS, FORCE_MSG, START_MSG, CUSTOM_CAPTION, DISABLE_CHANNEL_BUTTON, PROTECT_CONTENT, DELAY

from helper_func import subscribed, encode, decode, get_messages
from database.database import add_user, del_user, full_userbase, present_user, fsub, req_db
from plugins.req_count import add_req, del_req, show_req, join_reqs, reset_req

async def delete_message_after_delay(client: Client, chat_id: int, message_id: int, delay: int):
    await asyncio.sleep(delay)
    try:
        await client.delete_messages(chat_id, message_id)
    except Exception as e:
        print(f"Error deleting message {message_id} in chat {chat_id}: {e}")

@Bot.on_message(filters.command('start') & filters.private & subscribed)
async def start_command(client: Client, message: Message):
    id = message.from_user.id
    if not await present_user(id):
        try:
            await add_user(id)
        except:
            pass
    text = message.text
    if len(text) > 7:
        await message.delete()
        try:
            base64_string = text.split(" ", 1)[1]
        except:
            return
        string = await decode(base64_string)
        argument = string.split("-")
        if len(argument) == 3:
            try:
                start = int(int(argument[1]) / abs(client.db_channel.id))
                end = int(int(argument[2]) / abs(client.db_channel.id))
            except:
                return
            if start <= end:
                ids = range(start, end + 1)
            else:
                ids = []
                i = start
                while True:
                    ids.append(i)
                    i -= 1
                    if i < end:
                        break
        elif len(argument) == 2:
            try:
                ids = [int(int(argument[1]) / abs(client.db_channel.id))]
            except:
                return
        temp_msg = await message.reply("Please wait...")
        try:
            messages = await get_messages(client, ids)
        except:
            await message.reply_text("Something went wrong..!")
            return
        await temp_msg.delete()

        for msg in messages:
            if bool(CUSTOM_CAPTION) & bool(msg.document):
                caption = CUSTOM_CAPTION.format(
                    previouscaption="" if not msg.caption else msg.caption.html,
                    filename=msg.document.file_name
                )
            else:
                caption = "" if not msg.caption else msg.caption.html

            if DISABLE_CHANNEL_BUTTON:
                reply_markup = msg.reply_markup
            else:
                reply_markup = None

            try:
                sent_message = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                asyncio.create_task(delete_message_after_delay(client, message.from_user.id, sent_message.id, int(DELAY)))
                await asyncio.sleep(1)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_message = await msg.copy(
                    chat_id=message.from_user.id,
                    caption=caption,
                    parse_mode=ParseMode.HTML,
                    reply_markup=reply_markup,
                    protect_content=PROTECT_CONTENT
                )
                asyncio.create_task(delete_message_after_delay(client, message.from_user.id, sent_message.id, int(DELAY)))
            except Exception as e:
                print(f"Error sending message: {e}")
        n_msg = await message.reply("<blockquote><b>🔴 Before downloading the files, please transfer them to another location or save them in Saved Messages. They will be deleted in 60 minutes.</b></blockquote>")
        await asyncio.sleep(60)
        await n_msg.delete()
        return
    else:
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("📯 About Me", callback_data="about"),
                    InlineKeyboardButton("📴 Close", callback_data="close")
                ]
            ]
        )
        await message.reply_text(
            text=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=None if not message.from_user.username else '@' + message.from_user.username,
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=reply_markup,
            disable_web_page_preview=True,
            quote=True
        )
        return


WAIT_MSG = """"<b>Processing ...</b>"""

REPLY_ERROR = """<blockquote><b>Use this command as a reply to any telegram message without any spaces.</b></blockquote>"""


@Bot.on_message(filters.command('start') & filters.private)
async def not_joined(client: Client, message: Message):
    buttons = []

    bot_id = client.me.id
    fsub_entry = fsub.find_one({"_id": bot_id})
    req_entry = req_db.find({})

    force_sub_channels = fsub_entry.get("channel_ids", []) if fsub_entry else []
    req_channels = [entry["_id"] for entry in req_entry]

    all_channels = list(set(force_sub_channels + req_channels))

    for idx, channel_id in enumerate(all_channels, start=1):
        try:
            if channel_id in force_sub_channels:
                invite_link = await client.create_chat_invite_link(chat_id=int(channel_id), creates_join_request=False)
            else:
                invite_link = await client.create_chat_invite_link(chat_id=int(channel_id), creates_join_request=True)
            buttons.append(
                InlineKeyboardButton(
                    f"Join {idx}",
                    url=invite_link.invite_link
                )
            )
        except Exception as e:
            print(f"Error creating invite link for channel {channel_id}: {e}")

    button1, button2 = [], []
    for i, button in enumerate(buttons):
        if i % 2 == 0:
            button1.append(button)
        else:
            button2.append(button)

    newbuttons = []
    if button1 and button2:
        for btn1, btn2 in zip(button1, button2):
            newbuttons.append([btn1, btn2])

    if len(button1) > len(button2):
        newbuttons.append([button1[-1]])

    try:
        newbuttons.append(
            [
                InlineKeyboardButton(
                    text='Try Again',
                    url=f"https://t.me/{client.username}?start={message.command[1]}"
                )
            ]
        )
    except IndexError:
        pass

    await message.reply(
        text=FORCE_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username=None if not message.from_user.username else '@' + message.from_user.username,
            mention=message.from_user.mention,
            id=message.from_user.id
        ),
        reply_markup=InlineKeyboardMarkup(newbuttons),
        quote=True,
        disable_web_page_preview=True
    )

@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0
        
        pls_wait = await message.reply("<i>Broadcasting Message.. This will Take Some Time</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
                pass
            total += 1
        
        status = f"""<b><u>Broadcast Completed</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""
        
        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

# Handlers for Force Subscription
@Bot.on_message(filters.command('addfsub') & filters.private & filters.user(ADMINS))
async def add_fsub(client, message):
    if len(message.command) == 1:
        await message.reply("Please provide channel IDs to add as fsub in the bot. If adding more than one, separate IDs with spaces.")
        return

    channel_ids = message.text.split()[1:]
    bot_id = client.me.id

    for channel_id in channel_ids:
        try:
            test_msg = await client.send_message(int(channel_id), "test")
            await test_msg.delete()
        except Exception as e:
            await message.reply(f"Please make the bot an admin in channel_id: {channel_id} or double-check the id. Error: {e}")
            return

    fsub.update_one(
        {"_id": bot_id},
        {"$addToSet": {"channel_ids": {"$each": channel_ids}}},
        upsert=True
    )
    await message.reply(f"Added channel IDs: {', '.join(channel_ids)}")

@Bot.on_message(filters.command('delfsub') & filters.private & filters.user(ADMINS))
async def del_fsub(client, message):
    if len(message.command) == 1:
        await message.reply("Please provide channel IDs to delete from fsub in the bot. If deleting more than one, separate IDs with spaces.")
        return

    channel_ids = message.text.split()[1:]
    bot_id = client.me.id

    fsub.update_one(
        {"_id": bot_id},
        {"$pull": {"channel_ids": {"$in": channel_ids}}}
    )
    await message.reply(f"Deleted channel IDs: {', '.join(channel_ids)}")

@Bot.on_message(filters.command('showfsub') & filters.private & filters.user(ADMINS))
async def show_fsub(client, message):
    bot_id = client.me.id
    fsub_entry = fsub.find_one({"_id": bot_id})
    req_entries = req_db.find({})

    force_sub_channels = fsub_entry.get("channel_ids", []) if fsub_entry else []
    req_channels = [entry["_id"] for entry in req_entries]

    all_channels = list(set(force_sub_channels + req_channels))

    channel_info = []
    for channel_id in all_channels:
        user_count = len(req_db.find_one({"_id": channel_id}).get("User_INFO", [])) if req_db.find_one({"_id": channel_id}) else 0
        try:
            chat = await client.get_chat(int(channel_id))
            channel_info.append(f"→ **[{chat.title}]({chat.invite_link})**: {user_count} user requests")
        except Exception as e:
            channel_info.append(f"→ **Channel ID: {channel_id}**: {user_count} users (Error: {e})")

    if channel_info:
        await message.reply(f"**Channels Added For Subscription:**\n" + "\n".join(channel_info), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:
        await message.reply("No subscribed channels found.")
