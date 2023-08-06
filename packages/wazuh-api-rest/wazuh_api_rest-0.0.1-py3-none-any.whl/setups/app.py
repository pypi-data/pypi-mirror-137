from api import api_router
from setups.config import AppConfig
from fastapi import FastAPI

app = FastAPI(title=AppConfig.PROJECT_NAME)
app.include_router(api_router, prefix=AppConfig.API_PREFIX)
