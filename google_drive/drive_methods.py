#===========================# 
#        Description        #
#===========================#
# Contains all the functions that use the Google Drive API
import os
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from io import BytesIO

# Import Create_Service from the local package module
from .Google import Create_Service

# Resolve paths relative to this module for robustness
BASE_DIR = os.path.dirname(__file__)
CLIENT_SECRET_FILE = os.path.join(BASE_DIR, 'credentials.json')
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

# ID of 'Sound Sensor Project Data' folder in my Google Drive
folder_id = '1APyRc2jRlgCXxGahNn2NbBI2EJf-2fEe'

## seeing the methods available to the Google Drive service
# print(dir(service))

#===========================# 
#        File Upload        #
#===========================#
# Uploads a file from my local recordings directory into the designated Google Drive folder
def file_upload(filename):
    # Accept either a full path or a path relative to the project/recordings directory
    # Normalize to an absolute file path
    if os.path.isabs(filename):
        filepath = filename
    else:
        # If the caller passes a path that already includes the recordings folder, use it
        candidate = os.path.join(BASE_DIR, filename)
        if os.path.exists(candidate):
            filepath = candidate
        else:
            # Fallback to recordings/<filename>
            filepath = os.path.join(BASE_DIR, 'recordings', os.path.basename(filename))

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File to upload not found: {filepath}")

    file_metadata = {
        'name': os.path.basename(filepath),
        'parents': [folder_id]
    }

    media = MediaFileUpload(filepath, mimetype='audio/wav')
    service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id'
    ).execute()
    print("File Successfully Uploaded!")


#===========================# 
#        List Files         #
#===========================#
# Returns a list of the n most recent files from the recording
def list_most_recent(n):
    query =f"parents = '{folder_id}'"
    response = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
    files = response.get('files', [])
    nextPageToken = response.get('nextPageToken')

    # returns null if there is only one page of recordings
    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken, 
                                        fields="files(id, name, createdTime)").execute()
        files.extend(response.get('files'))
        nextPageToken= response.get('nextPageToken')

    # sort the files by createdTime
    sorted_files = sorted(files, key=lambda x: x['createdTime'], reverse=True)

    # get the 3 most recent files
    recent_files = sorted_files[:n]
    # test = []

    # for files in recent_files:
    #     test.append(files['name'])
        
    # return a list of the desired number of files 
    return recent_files

#===========================# 
# Files From a Specific Day #
#===========================#
# Returns all the files with the same creation date 
def recordings_on_day(creation_date):
    # creation_date should be a string like "2026-06-15"
    start = f"{creation_date}T00:00:00"
    end = f"{creation_date}T23:59:59"
    
    query = f"parents = '{folder_id}' and createdTime >= '{start}' and createdTime <= '{end}'"
    response = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
    files = response.get('files', [])

    nextPageToken = response.get('nextPageToken')
    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken,
                                        fields="files(id, name, createdTime)").execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')

    return files

#===========================# 
# Files From a Specific Day #
#===========================#
# Middleman that makes a Google Drive API call to download the .wav file content
# BytesIO is an in-memory buffer, it's a temporary container that holds the downloaded bytes in RAM 
# so StreamingResponse can read from it and forward them to the browser.
def get_file_stream(file_id):
    buffer = BytesIO()
    request = service.files().get_media(fileId=file_id)

    # a Drive API helper that handles the downloading, writing chunks into the buffer as they arrive
    downloader = MediaIoBaseDownload(buffer, request)

    done = False
    while not done:
        # _, discards the progress status (don't need it here)
        _, done = downloader.next_chunk()

    # buffer cursor is at the end after writing, puts it back to the start so that StreamingResponse
    # reads it from the start
    buffer.seek(0)
    return buffer
    