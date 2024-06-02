from fastapi import APIRouter


router = APIRouter(
    prefix="/education",
    tags=["education"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def get_education():
     return {"message": "Hello Education Applications!"}