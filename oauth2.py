from fastapi import FastAPI, HTTPException, Depends
from authlib.integrations.starlette_client import OAuth
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Google OAuth Configuration
GOOGLE_CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"

class User(BaseModel):
    name: str
    email: str
    picture: str

oauth = OAuth()
oauth.register(
    name="google",
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    client_kwargs={"scope": "openid email profile"},
)

def verify_google_token(token: str):
    """Verify Google ID token"""
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=403, detail="Invalid token")
    return response.json()

@app.post("/auth/google")
async def google_auth(token: str):
    """Authenticate user with Google token"""
    user_info = verify_google_token(token)
    user = User(
        name=user_info["name"],
        email=user_info["email"],
        picture=user_info["picture"]
    )
    return {"message": "User authenticated", "user": user.dict()}
