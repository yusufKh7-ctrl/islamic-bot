from telegram import Message
from telegram.error import BadRequest


async def send_split_message(message: Message, text: str, max_length: int = 4000, **kwargs):
    if len(text) <= max_length:
        await message.reply_text(text, **kwargs)
        return


    lines = text.split("\n")
    current_chunk = ""

    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            try:
                await message.reply_text(current_chunk, **kwargs)
            except BadRequest: 
                await message.reply_text(current_chunk)

            current_chunk = line + "\n"
        else:
            current_chunk += line + "\n"

    if current_chunk.strip():
        try:
            await message.reply_text(current_chunk, **kwargs)
        except BadRequest:
            await message.reply_text(current_chunk)

