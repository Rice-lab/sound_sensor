#===========================# 
#        Description        #
#===========================#
# Main file that contains the webapp
# App Initialization and Structure, (API) Endpoints
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

# Extra Imports
from pathlib import Path
from google_drive.drive_methods import list_most_recent, get_file_stream, recordings_on_day
from datetime import date
import calendar

app = FastAPI()
app.mount("/static", StaticFiles(directory=Path(__file__).parent /"static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent /"templates")

#===========================# 
#        Endpoints          #
#===========================#
@app.get("/", include_in_schema=False)
def home(request: Request):
    # Fetch the three most recent recordings every time the page is loaded
    recent = list_most_recent(3)

    # third arg is the context dictionary, template can access anything in it
    return templates.TemplateResponse(request, 
                                      "home.html", 
                                      {"title": "Home",
                                       "recent_files": recent},)

# temporarily we'll have 2 directories from home: Recordings and Analytics
# can add more if need be
@app.get("/recordings", include_in_schema=False)
def recordings(request: Request, month: int=None, year: int=None):
    # Upon landing, we want the user to have the current month's calendar open
    # We'll only worry about one year worth of recordings
    today  = date.today()
    year = year or today.year
    month = month or today.month
    cal = calendar.Calendar(firstweekday=6).monthdayscalendar(year, month)
    month_name = calendar.month_name[month]
    
    return templates.TemplateResponse(request, 
                                      "recordings.html", 
                                      {"title": "Recordings",
                                       "calendar": cal,
                                       "year": year,
                                       "month": month,
                                       "month_name": month_name},)

# Returns all the recordings for the day the user clicks on in the calendar
@app.get("/recordings/{year}/{month}/{day}", include_in_schema=False)
def day_recordings(request: Request, year: str, month: str, day: str):
    clicked_date = year + "-" + month + "-" + day
    files = recordings_on_day(clicked_date)
    return templates.TemplateResponse(request,
                                      "recordings_onDay.html",
                                      {"title": clicked_date,
                                       "files": files},)

@app.get("/analytics", include_in_schema=False)
def analytics(request: Request):
    return templates.TemplateResponse(request, 
                                      "analytics.html", 
                                      { "title": "Analytics"},)


#===========================# 
#       API Endpoints       #
#===========================#
# API Directories (json)
# Fetching the recordings
@app.get("/api/audio/{file_id}")
def play_recordings(file_id: str):
    buffer = get_file_stream(file_id)
    return StreamingResponse(buffer, media_type="audio/wav")

