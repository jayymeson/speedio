from fastapi import FastAPI
from routes.handler import router

app = FastAPI()
app.include_router(router)
