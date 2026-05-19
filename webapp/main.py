from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# structure of the app
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

@app.get("/", include_in_schema=False)
def home(request: Request):
    # third arg is the context dictionary, template can access anything in it
    return templates.TemplateResponse(request, "home.html", {"headers": headers} )

# temporarily we'll have 2 directories from home: Recordings and Analytics
# can add more if need be

# for api directories (JSON)
@app.get("/api/temp")
def temp():
    return headers