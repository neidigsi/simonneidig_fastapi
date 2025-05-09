# Import external dependencies
from fastapi import FastAPI

# Import internal dependencies
from app.api.routes.contact import contact
from app.api.routes.education import education
from app.api.routes.experience import experience
from app.api.routes.expertise import expertise
from app.api.routes.page import page
from app.api.routes.personal_details import personal_details
from app.api.routes.personal_information import personal_information
from app.api.routes.social_media import social_media
from app.api.routes.work import work


# Initialize FastAPI app
app = FastAPI()

# Add routes to FastAPI app
app.include_router(contact.router)
app.include_router(education.router)
app.include_router(experience.router)
app.include_router(expertise.router)
app.include_router(page.router)
app.include_router(personal_details.router)
app.include_router(personal_information.router)
app.include_router(social_media.router)
app.include_router(work.router)
