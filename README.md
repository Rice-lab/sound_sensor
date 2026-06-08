# Python Sound Recording System
## Overview
A sound-recording system that detects when a certain sound threshold is breached and automatically starts recording after through a Python program. The recordings are sent to my personal gmail through Google Drive Api. The system is accompanied by a webapp made in FastAPI which allows me to view and play the recordings and gather analytics through AI. I'm hoping to replace the Python program with an ESP32 once the main functional components work properly. 

## Audio Recorder
### Features
Under Construction!
### How to Run
The code for auto-recording is located in _auto_record.py_ and can be run by typing the following in terminal:
```
python -m auto_record.py
```
The other scripts in the directory include:
- _test.py_ - File I used for testing functions
- _audio.py_ - File for basic recording
- _auto_record.py_ - File I'm planning to use to handle uploading the recordings to Google Drive
## WebApp
### Features
Under Construction!
### How to Run
_main.py_ can be found in the "webapp" directory and be run in dev mode by typing the following in terminal while in the root directory:
```
python -m uvicorn webapp.main:app --reload
```
... or it can also be run in production mode through the following: 
```
python -m uvicorn webapp.main:app
```
## Google Drive
### Features
Under Construction!
### How to Run
This folder only contains the functions that the Audio Recorder and Webapp call but if you want to test individual Drive API functions then call it as such: 
```
python -m google_drive.<filename>
```


