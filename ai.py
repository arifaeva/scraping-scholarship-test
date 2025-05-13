# ai.py
from openai import OpenAI
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from enum import Enum

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class StudyLevel(str, Enum):
    S1 = "S1"
    S2 = "S2"
    S3 = "S3"

class ScholarshipType(str, Enum):
    partially_funded = "Partially Funded"
    fully_funded = "Fully Funded"

class Scholarship(BaseModel):
    name: str
    country: str
    scholarship_type: ScholarshipType
    study_level: StudyLevel
    start_date: str
    end_date: str
    description: str
    requirements: str
    benefit: str
    url: str  

class ScholarshipList(BaseModel):
    scholarships: list[Scholarship]