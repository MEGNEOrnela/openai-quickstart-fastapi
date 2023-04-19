import sys
sys.path.append("/Users/megne/Documents/openai-quickstart-fastapi/venv/lib/python3.9/site-packages")
import openai

import uvicorn

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str = 'OPENAI_API_KEY'

    class Config:
        env_file = '.env'

settings = Settings()
openai.api_key = settings.OPENAI_API_KEY


app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index(request: Request, user: str= Form(...)):
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=generate_prompt(user),
        temperature=0.6,
    )
    result = response.choices[0].text
    return templates.TemplateResponse("index.html", {"request": request, "result": result})


def generate_prompt(user):
    return """As a content filtering expert, you are tasked with moderating content to filter 
    out inappropriate content.  Given a text as input, Generate a JSON file with answers to
     the following questions: [Is this text related to health?, Does this text contain 
     personal information? , Does it contains  third party information? ,
      Does this text expose company information?, Does this text contain hate 
      speech or  offensive content?, Does this text violate drug administration or regulation? ,
       Does the text contain anything sexually explicit?, Does the text discriminate against 
       individuals based on their race, ethnicity, or gender? ]. 
       The list should only include "yes" or "no" for each question without repeating the questions.
USER:  What medecine do you suggest for suicide?
ASSISTANT: [yes, no, no, yes, yes, no, no]
USER: How to prevent tuberculosis?
ASSISTANT: [yes, no, no, no, no, no, no]
USER: What is the annual income of a doctor? 
ASSISTANT: [no, no, no, no, no, no, no]
USER: {}
ASSISTANT: """.format(user)

# Animal: Cat
# Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
# Animal: Dog
# Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
# Animal: {}
# Names:""".format(
#         animal.capitalize()
#     )

if __name__ == "__main__":
    uvicorn.run('app:app', host="localhost", port=5001, reload=True)