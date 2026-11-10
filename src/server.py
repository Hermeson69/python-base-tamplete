import asyncio

import uvicorn
from .core.config import validate_env
from .db import init_db



def run() -> None:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    loop.close()
    uvicorn.run("src.api:app", host="0.0.0.0", port=8080, log_level="info")


