from fastapi import FastAPI

from api.routes.education import education

app = FastAPI()

app.include_router(education.router)

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}