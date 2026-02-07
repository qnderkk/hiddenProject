from pydantic import BaseModel, Field, EmailStr


class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, description="Name of the sender")
    email: EmailStr = Field(..., description="Email of the sender")
    subject: str = Field(..., description="Topic: 'Complaint', 'Question', 'Suggestion'")
    message: str = Field(..., min_length=2, description="Text of the message")