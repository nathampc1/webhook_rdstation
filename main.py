from fastapi import FastAPI
import logging
import models
import API

settings = models.Settings()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RD Station Webhook Processor",
    description="Receber webhook rd station"
)


@app.post("/webhook-rdstation/", response_model=models.NewRequestData)
async def webhook_endpoint(data: models.RDStationWebhook):
    return await API.webhook_processor(data, settings.TARGET_URL, logger)