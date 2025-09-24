from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
from pydantic_settings import BaseSettings
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

origins = [
    'http://localhost:3000',
    'https://ricardo272727.github.io'
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class Settings(BaseSettings):
    BRAVO_API_KEY: str = ""

settings = Settings()


class Contact(BaseModel):
    fullName: str
    email: str
    company: str
    projectType: str
    projectDetails: str

@app.post("/contact")
def contact(contact: Contact):
    response = requests.post("https://api.brevo.com/v3/smtp/email", headers={
        "Accept": "application/json",
        "api-key": settings.BRAVO_API_KEY,
    }, data=json.dumps({
       "sender":{
          "name": contact.fullName,
          "email": contact.email,
       },
       "to":[
          {
             "email": "cuanaloricardo@gmail.com",
             "name": "Ricardo Cuanalo"
          }
       ],
       "subject": "Contact from Portfolio Page",
       "htmlContent": f"""
       <html><head></head><body>
       <h2>Name: {contact.fullName}</h2>
       <h2>Email: {contact.email}</h2>
       <h2>Company: {contact.company}</h2>
       <h2>Project type: {contact.projectType}</h2>
       <p>Project details: {contact.projectDetails}</p>
       </body></html>
       """
    }))
    print(response.json())
    return contact

