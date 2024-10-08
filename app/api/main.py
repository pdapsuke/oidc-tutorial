from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import routers

app = FastAPI()

app.include_router(routers.router, prefix="/api/v1")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)