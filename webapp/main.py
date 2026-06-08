#===========================# 
#        Description        #
#===========================#
# Main file that contains the webapp
# App Initialization and Structure, (API) Endpoints
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path
from google_drive.drive_methods import list_most_recent

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent /"static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent /"templates")

# Required Lists
headers: list[dict] = [
    {
        "title": "Recordings", 
        "subheader": "View and play recordings here"
    },
    {
        "title": "Analytics",
        "subheader": "Uses AI to parse information from metadata"
    }
]

test = list_most_recent(3)

#===========================# 
#        Endpoints          #
#===========================#
@app.get("/", include_in_schema=False)
def home(request: Request):
    # third arg is the context dictionary, template can access anything in it
    return templates.TemplateResponse(request, 
                                      "home.html", 
                                      {"headers": headers, "title": "Home",
                                       "test": test},)

# temporarily we'll have 2 directories from home: Recordings and Analytics
# can add more if need be
@app.get("/recordings", include_in_schema=False)
def recordings(request: Request):
    return templates.TemplateResponse(request, 
                                      "recordings.html", 
                                      {"headers": headers, "title": "Home"},)

@app.get("/analytics", include_in_schema=False)
def analytics(request: Request):
    return templates.TemplateResponse(request, 
                                      "analytics.html", 
                                      {"headers": headers, "title": "Home"},)


#===========================# 
#       API Endpoints       #
#===========================#
# API Directories (json)
@app.get("/api/temp")
def temp():
    return headers