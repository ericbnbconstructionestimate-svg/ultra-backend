from fastapi import APIRouter, HTTPException, Depends
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import json, os
from sqlalchemy.orm import Session
from app.db import get_db
from app import models
from app.core.config import settings

router = APIRouter(tags=["gmail"])

@router.get("/auth/start")
def auth_start():
    if not os.path.exists(settings.CREDENTIALS_FILE):
        raise HTTPException(500, "Missing credentials.json")
    flow = Flow.from_client_secrets_file(
        settings.CREDENTIALS_FILE,
        scopes=[
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        redirect_uri=settings.OAUTH_REDIRECT_URI
    )
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    with open("oauth_state.json", "w") as f:
        f.write(json.dumps({"state": state}))
    return {"auth_url": auth_url}

@router.get("/auth/callback")
def auth_callback(code: str, state: str, db: Session = Depends(get_db)):
    if not os.path.exists(settings.CREDENTIALS_FILE):
        raise HTTPException(500, "Missing credentials.json")
    saved = {}
    if os.path.exists("oauth_state.json"):
        saved = json.load(open("oauth_state.json"))
    flow = Flow.from_client_secrets_file(
        settings.CREDENTIALS_FILE,
        scopes=[
            "https://www.googleapis.com/auth/gmail.send",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid"
        ],
        redirect_uri=settings.OAUTH_REDIRECT_URI
    )
    flow.fetch_token(code=code)
    creds = flow.credentials
    oauth2 = build('oauth2', 'v2', credentials=creds, cache_discovery=False)
    info = oauth2.userinfo().get().execute()
    email = info.get("email")
    acc = models.Account(email=email, creds_json=creds.to_json())
    db.add(acc)
    db.commit()
    return "<h3>Connected</h3>"
