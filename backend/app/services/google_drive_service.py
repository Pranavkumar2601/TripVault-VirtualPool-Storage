from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload


from app.models.user_cloud_account import UserCloudAccount


def get_drive_client(account: UserCloudAccount):
    creds = Credentials(
        token=account.access_token,
        refresh_token=account.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=None,       # handled internally
        client_secret=None,
        scopes=["https://www.googleapis.com/auth/drive.appdata"],
    )

    return build("drive", "v3", credentials=creds)


# To create app folder in Google Drive AppData
def ensure_app_folder(drive):
      
      """
    Creates (or retrieves) the TripVault app folder
    inside Google Drive AppData.
    """
    #   Search for existing folder
      response = drive.files().list(
         spaces="appDataFolder",
         q ="name='TripVault' and mimeType='application/vnd.google-apps.folder'",
         fields="files(id,name)",
    ).execute()
      
      files =response.get("files", [])
      if files:
            return files[0]["id"]
      
    #   create folder if not exists

      file_metadata={
         "name": "TripVault",
            "mimeType": "application/vnd.google-apps.folder",
            "parents": ["appDataFolder"],

    }
      
      folder= drive.files().create(
           body=file_metadata,
           fields="id",
      ).execute()

      return folder["id"]

#  real upload helper to Google Drive service

def upload_chunk_to_drive(
    drive,
    *,
    folder_id: str,
    chunk_name: str,
    data: bytes,
):
    media = MediaInMemoryUpload(
        data,
        mimetype="application/octet-stream",
        resumable=False,
    )

    file_metadata = {
        "name": chunk_name,
        "parents": [folder_id],
    }

    file = drive.files().create(
        body=file_metadata,
        media_body=media,
        fields="id",
    ).execute()

    return file["id"]
