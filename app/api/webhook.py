from fastapi import APIRouter, Request, Response, status
from telegram import Update
from app.islamic_bot import ptb_app, logger

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/webhook")
async def telegram_webhook(req: Request):
    try:
        data = await req.json()
        update = Update.de_json(data, ptb_app.bot)
        await ptb_app.process_update(update)
        return Response(status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Error processing webhook update: {e}", exc_info=True)
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
