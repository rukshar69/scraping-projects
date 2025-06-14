from typing import Optional
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_cohere import ChatCohere


# --------------- Load environment variables --------------- #
load_dotenv()  # Loads from .env file in current working directory

# Ensure the API key is available
api_key = os.getenv("COHERE_API_KEY")
if not api_key:
    raise EnvironmentError("Missing COHERE_API_KEY in environment or .env file.")

class JobDescriptionSchema(BaseModel):
    job_responsibilities: str = Field(
        ...,
        description="Section of the job description detailing key responsibilities."
    )
    job_requirements: str = Field(
        ...,
        description="Section of the job description outlining required skills, qualifications, or expertise."
    )
    company_name: Optional[str] = Field(
        None,
        description="The name of the company offering the job, if mentioned."
    )
    company_address: Optional[str] = Field(
        None,
        description="Company address or location, if explicitly stated."
    )
    application_email: Optional[str] = Field(
        None,
        description="Email address where resumes should be sent, if provided."
    )
    benefits: Optional[str] = Field(
        None,
        description="Details about benefits offered for the position, if mentioned."
    )
    compensation: Optional[str] = Field(
        None,
        description="Information about salary or compensation, if provided."
    )

# Define the prompt template with a placeholder for job_description
prompt = PromptTemplate.from_template(
    """You are an expert job description analyzer. Given a raw job description, extract the following:
    - job_responsibilities
    - job_requirements
    - company_name
    - company_address
    - application_email
    - benefits
    - compensation

    Job Description:
    {job_description}
    """
    )

llm = ChatCohere(model="command-a-03-2025", api_key=api_key)
structured_llm = llm.with_structured_output(JobDescriptionSchema)

def extract_job_info(job_description: str) -> dict:
    """
    Extracts structured information from a job description.
    
    :param job_description: The raw text of the job listing
    :return: Dictionary with parsed fields
    """
    try:
        formatted_prompt = prompt.format(job_description=job_description)
        response = structured_llm.invoke(formatted_prompt)
        return response
    except Exception as e:
        return {"error": str(e)}


