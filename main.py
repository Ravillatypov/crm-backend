import uvicorn
from fastapi import FastAPI
from tortoise import Tortoise

from app.routers import routes
from app.settings import DB_DSN

app = FastAPI(title='CRM')

for prefix, router in routes:
    app.include_router(router, prefix=prefix)


@app.on_event('startup')
async def startup():
    await Tortoise.init(
        db_url=DB_DSN,
        modules={
            'auth': ['app.auth.models'],
        }
    )
    await Tortoise.generate_schemas()


@app.on_event('shutdown')
async def shutdown():
    await Tortoise.close_connections()


if __name__ == '__main__':
    uvicorn.run(app)
