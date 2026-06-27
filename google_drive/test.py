# Testing file uploads - Works!
from .Google import Create_Service
from googleapiclient.http import MediaFileUpload
from .drive_methods import file_upload, list_most_recent, get_file_stream
from .drive_methods import recordings_on_day
CLIENT_SECRET_FILE = './google_drive/credentials.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive.file']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

## seeing the methods available to the Google Drive service
# print(dir(service))

folder_id = '1APyRc2jRlgCXxGahNn2NbBI2EJf-2fEe'


# #===========================# 
# #        File Upload        #
# #===========================#
# # Testing code to upload file from local to Drive

# # In this section he hardcoded the names of the files in the names list
# # I'll do the same initially just to verify that it works but we need to make it dynamic

# file_names = ['recording_May_22_2026_10-59-40.wav']
# mime_types = ['audio/wav']

# for file_name, mime_type in zip(file_names, mime_types):
#     file_metadata = {
#         'name': file_name,
#         'parents': [folder_id]
#     }

# media = MediaFileUpload('./recordings/{0}'.format(file_name), mimetype=mime_type)
# service.files().create(
#     body=file_metadata, 
#     media_body=media,
#     fields='id'
# ).execute()

# #===========================# 
# #        List Files         #
# #===========================#
# # Testing the code to list files from the recordings folder in the Drive

# # creates a Google Drive API filter string
# # give me all the files whose parent folder is folder_id 
# query =f"parents = '{folder_id}'"

# # .files selects the files resource of the API as opposed to drives or permissions
# # .list constructs a request object which packages your parameters
# # .execute takes the prepared request and sends an HTTP GET request to Google's servers
# response = service.files().list(q=query).execute()

# # pulls out the list of file objects from the response
# files = response.get('files')

# # checks if there are more pages of results 
# # Google Drive caps results per request (default 100) so 
# # if there are more files it returns a token pointing to the 
# # next page, None if there are no more pages
# nextPageToken = response.get('nextPageToken')

# # loop stops when nextPageToken comes back as None
# # each iteration fetches the next batch and appends it to files 
# # using .extend()
# while nextPageToken:
#     response = service.files().list(q=query, pageToken=nextPageToken).execute()
#     files.extend(response.get('files'))
#     nextPageToken= response.get('nextPageToken')

# # print the name and the mimeType of each file in the folder
# for f in files:
#     print(f['name'], f['mimeType'])

# test = list_most_recent(1)
# for x in test:
#     print(x)

# file_id = test[0]['id']
# buffer = get_file_stream(file_id)
# with open("test_output.wav", "wb") as f:
#     f.write(buffer.read())

# print("Done")

test = recordings_on_day("2026-05-26")
print(test)