import uvicorn

from app.config import settings
from app.log import get_logger

log = get_logger(__name__)

if __name__ == "__main__":
    log.info(f"Server started at {settings.SERVER_HOST}:{settings.SERVER_PORT}")
    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
