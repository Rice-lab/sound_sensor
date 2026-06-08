#===========================# 
#        Description        #
#===========================#
# Contains all the functions that use the Google Drive API
import os
from googleapiclient.http import MediaFileUpload

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

    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken= response.get('nextPageToken')

    # sort the files by createdTime
    sorted_files = sorted(files, key=lambda x: x['createdTime'], reverse=True)

    # get the 3 most recent files
    recent_files = sorted_files[:n]
    test = []

    for files in recent_files:
        test.append(files['name'])
        
    # return a list of the desired number of files 
    return test


