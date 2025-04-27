# Import external dependencies
from fastapi import FastAPI

# Import internal dependencies
from app.api.routes.education import education
from app.api.routes.experience import experience


# Initialize FastAPI app
app = FastAPI()

# Add routes to FastAPI app
app.include_router(education.router)
app.include_router(experience.router)
