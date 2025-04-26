# Import external dependencies
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Import internal dependencies
from app.db.database import Base


class InstitutionTransation(Base):
    __tablename__ = "institution_translation"

    # Primary key
    id = Column(Integer, primary_key=True)
    
    # Content
    name = Column(String)
    
    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))
    language_id = Column(Integer, ForeignKey("language.id"))

    # Establishing relationships
    institution = relationship(
        "Institution", back_populates="translations")
    language = relationship(
        "Language", back_populates="institution_translations")
