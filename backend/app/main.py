import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.routes.users import users_router
from app.data.database import sessionmanager

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    # Create database tables on startup
    await sessionmanager.create_db_and_tables()
    
    yield
    
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="Delphi Candidate Screen Recording Service", docs_url="/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# Routers
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)