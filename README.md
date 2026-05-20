# Python Sound Recording System
## Overview
A sound-recording system that detects when a certain sound threshold is breached and automatically starts recording after through a Python program. The recordings are sent to my personal gmail through Google Drive Api. The system is accompanied by a webapp made in FastAPI which allows me to view and play the recordings and gather analytics through AI. I'm hoping to replace the Python program with an ESP32 once the main functional components work properly. 
## How to Run
### Audio Recorder
The code for auto-recording is located in _auto_record.py_ and can be run by typing the following in terminal:
```
python3 auto_record.py
```
The other scripts in the directory include:
- _test.py_ - File I used for testing functions
- _audio.py_ - File for basic recording
- _GDfile_upload.py_ - File I'm planning to use to handle uploading the recordings to Google Drive
### WebApp
_main.py_ can be found in the "webapp" directory and be run in dev mode by typing the following in terminal:
```
python -m fastapi dev main.py
```
... or it can also be run in production mode through the following: 
```
python -m fastapi main.py
```

