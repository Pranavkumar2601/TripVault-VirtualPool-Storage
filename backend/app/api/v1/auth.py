from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from google_auth_oauthlib.flow import Flow
import requests

from app.core.config import settings
from app.core.database import get_db
from app.models.user_cloud_account import UserCloudAccount
from app.services.google_drive_service import get_drive_client,ensure_app_folder

router = APIRouter(prefix="/auth", tags=["auth"])


GOOGLE_SCOPES = [
    "https://www.googleapis.com/auth/drive.appdata"
]


def get_oauth_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [settings.GOOGLE_REDIRECT_URI],
            }
        },
        scopes=GOOGLE_SCOPES,
        redirect_uri=settings.GOOGLE_REDIRECT_URI,
    )


# =========================
# 1. Login
# =========================
@router.get("/google/login")
def google_login(user_id: str = Query(...)):
    flow = get_oauth_flow()

    auth_url, _ = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
        state=user_id,  # 👈 bind OAuth to user
    )

    return RedirectResponse(auth_url)


# =========================
# 2. Callback
# =========================
@router.get("/google/callback")
def google_callback(
    code: str,
    state: str,  # this is user_id
    db: Session = Depends(get_db),
):
    user_id = state

    flow = get_oauth_flow()
    flow.fetch_token(code=code)

    creds = flow.credentials

    # Remove existing Google account if re-connecting
    db.query(UserCloudAccount).filter(
        UserCloudAccount.user_id == user_id,
        UserCloudAccount.provider == "google_drive",
    ).delete()

    account = UserCloudAccount(
        user_id=user_id,
        provider="google_drive",
        access_token=creds.token,
        refresh_token=creds.refresh_token,
        token_expiry=str(creds.expiry) if creds.expiry else None,
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    #  create app folder in user's drive
    drive = get_drive_client(account)
    folder_id = ensure_app_folder(drive)

    return {
        "message": "Google Drive connected successfully",
        "user_id": user_id,
        "app_folder_id": folder_id
    }
