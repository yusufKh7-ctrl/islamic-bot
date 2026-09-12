import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from app.api.webhook import router as webhook_router
from app.islamic_bot import ptb_app, logger

load_dotenv()

BASE_URL = os.getenv("WEBHOOK_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Telegram Bot...")
    await ptb_app.initialize()
    await ptb_app.start()

    if BASE_URL:
        webhook_path = f"{BASE_URL.rstrip('/')}/webhook"
        logger.info(f"Starting Webhook to: {webhook_path}")
        await ptb_app.bot.set_webhook(
            url=webhook_path,
            allowed_updates=["message"]
        )
    else:
        logger.warning("WEBHOOK is not set. Webhook was not registered.")

    yield

    logger.info("Stoping Telegram Bot...")
    await ptb_app.stop()
    await ptb_app.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/health")
@app.head("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(webhook_router)