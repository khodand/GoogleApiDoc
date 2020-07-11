from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


def create_copy_template_10():
    SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly', "https://www.googleapis.com/auth/drive"]

    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    document_id = "1fzM5sM0qybLAcek-G-w7PMPd3phDBNBS4S5Ds1SSPvQ"
    copy_title = 'Copy Template_10'
    body = {
        'name': copy_title
    }
    drive_response = service.files().copy(
        fileId=document_id, body=body).execute()
    document_copy_id = drive_response.get('id')
    return document_copy_id


def fill_template_10():
    DOCUMENT_ID = create_copy_template_10()
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly', "https://www.googleapis.com/auth/drive",
              "https://www.googleapis.com/auth/drive.file"]
    creds = None
    if os.path.exists('token1.pickle'):
        with open('token1.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials_docs.json', SCOPES)
            creds = flow.run_local_server()
        with open('token1.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('docs', 'v1', credentials=creds)

    custom_name = "Piter"
    custom_name1 = "Alice1"

    requests = []
    requests_names = ["cur", "cur1"]
    requests_respones = [custom_name, custom_name1]

    for i in range(len(requests_names)):
        requests.append({
            'replaceAllText': {
                'containsText': {
                    'text': '{{' + requests_names[i] + '}}',
                    'matchCase': "true"
                },
                'replaceText': requests_respones[i],
            }}
        )

        result = service.documents().batchUpdate(
            documentId=DOCUMENT_ID, body={'requests': requests}).execute()


