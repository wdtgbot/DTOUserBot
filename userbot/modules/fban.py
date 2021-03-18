
from sqlalchemy.exc import IntegrityError

from userbot import CMD_HELP, bot
from userbot.events import register
from userbot.cmdhelp import CmdHelp

@register(outgoing=True, disable_edited=True, pattern=r"^\.fban(?: |$)(.*)")
async def fban(event):
    """Fban."""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Sql modda işləyir!**")

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        fban_id = reply_msg.sender_id
        reason = event.pattern_match.group(1)
    else:
        pattern = str(event.pattern_match.group(1)).split()
        fban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        fban_id = await event.client.get_peer_id(fban_id)
    except:
        pass

    if event.sender_id == fban_id:
        return await event.edit(
            "**Xəta: Fban olunmadı**"
        )

    if len(fed_list := get_flist()) == 0:
        return await event.edit("**Heç bir federasiyanın admini deilsiz!**")

    user_link = f"[{fban_id}](tg://user?id={fban_id})"

    await event.edit(f"**Fban olunur** {user_link}...")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/fban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if (
                    ("Yeni FBAN" not in reply.text)
                    and ("Fban olunmağa başlayır" not in reply.text)
                    and ("Fban olunmağa başladı" not in reply.text)
                    and ("Fban səbəbi yeniləndi" not in reply.text)
                ):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Qeyd edilməmişdir."

    if failed:
        status = f"Failed to fban in {len(failed)}/{total} feds.\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Başa çatdı! {total} feddən fban oldu."

    await event.edit(
        f"**Fban edildi **{user_link}!\n**Səbəb:** {reason}\n**Status:** {status}"
    )


@register(outgoing=True, disable_edited=True, pattern=r"^\.unfban(?: |$)(.*)")
async def unfban(event):
    """Unfban"""
    try:
        from userbot.modules.sql_helper.fban_sql import get_flist
    except IntegrityError:
        return await event.edit("**Sql modda işləyir!**")

    if event.is_reply:
        reply_msg = await event.get_reply_message()
        unfban_id = reply_msg.sender_id
        reason = event.pattern_match.group(1)
    else:
        pattern = str(event.pattern_match.group(1)).split()
        unfban_id = pattern[0]
        reason = " ".join(pattern[1:])

    try:
        unfban_id = await event.client.get_peer_id(unfban_id)
    except:
        pass

    if event.sender_id == unfban_id:
        return await event.edit("**Gözləyin, bu qanunsuzdur**")

    if len(fed_list := get_flist()) == 0:
        return await event.edit("**Siz heçbir federasiyanın admini deilsiz!**")

    user_link = f"[{unfban_id}](tg://user?id={unfban_id})"

    await event.edit(f"**Fbandan çıxarıldı **{user_link}**...**")
    failed = []
    total = int(0)

    for i in fed_list:
        total += 1
        chat = int(i.chat_id)
        try:
            async with bot.conversation(chat) as conv:
                await conv.send_message(f"/unfban {user_link} {reason}")
                reply = await conv.get_response()
                await bot.send_read_acknowledge(
                    conv.chat_id, message=reply, clear_mentions=True
                )

                if (
                    ("Fbandan çıxarılma" not in reply.text)
                    and ("Fbandan çıxarıldı" not in reply.text)
                ):
                    failed.append(i.fed_name)
        except BaseException:
            failed.append(i.fed_name)

    reason = reason if reason else "Qeyd edilməmişdir."

    if failed:
        status = f"Fban açılmadı {len(failed)}/{total} .\n"
        for i in failed:
            status += "• " + i + "\n"
    else:
        status = f"Başa çatdı! {total} feddən fbandan çıxarıldı."

    reason = reason if reason else "Qeyd edilməmişdir."
    await event.edit(
        f"**UnFBAN** {user_link}!\n**Səbəb:** {reason}\n**Status:** {status}"
    )

CmdHelp('fban').add_command(
    'fban', None, 'Admin olduğunuz federasiyalardan banlıyar.'
).add_command(
    'unfban', None, 'Admin olduğunuz federasiyalardan bandan çıxardar.'
).add()
