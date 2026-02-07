from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from telegram import Bot
from telegram.error import TelegramError
from app.config import settings
from app.schemas.contact import ContactForm 
import textwrap
import traceback


router = APIRouter(prefix="/contacts", tags=["Contacts"])


telegram_bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)

async def send_to_telegram(message_text: str) -> bool:
    try:
        await telegram_bot.send_message(
            chat_id=settings.TELEGRAM_CHAT_ID,
            text=message_text,
            parse_mode="Markdown"
        )

        return True 
    
    except TelegramError as e:
        print(f"Error sending to Telegram: {e}")
        return False


def to_message(raw_message: ContactForm) -> str:
    if type(raw_message) == ContactForm:
        message_template = f"""
            *New message!*

            Name: {raw_message.name}
            Email: {raw_message.email}
            Subject: {raw_message.subject}
            Message: {raw_message.message}
        """
    else:
        raise HTTPException(status_code=404, detail="Invalid format of the data")
    
    processed_message = textwrap.dedent(message_template).strip()

    return processed_message


@router.post("/contact")
async def form_receiver(form_data: ContactForm):
    try:
        message = to_message(form_data)
        result = await send_to_telegram(message)

        if result is True:
            return {
                "status": "success",
                "message" : "Message has been sent"
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Error when sending a message: {result}"
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Form processing error: {traceback.format_exc()}"
        )
