from fastapi import FastAPI
from routers import notes, auth
import database_models
from database import engine




app = FastAPI()

app.include_router(notes.api)
app.include_router(auth.api)

@app.on_event("startup")
async def startup_event():
    print("Startup running")
    async with engine.begin() as conn:
        await conn.run_sync(database_models.Base.metadata.create_all)


@app.get("/")
def base():
    return "Base app" 

