import uvicorn
from fastapi import FastAPI

from app.routers import routes

app = FastAPI(title='CRM')
for prefix, router in routes:
    app.include_router(router, prefix=prefix)


if __name__ == '__main__':
    uvicorn.run(app)
