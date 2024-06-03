from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import supabase
import solventgpt.config as cfg

auth_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    try:
        token = credentials.credentials
        decoded_token = jwt.decode(token, cfg.JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def supa_login(username, password):
    supaclient = supabase.create_client(cfg.SUPABASE_URL, cfg.SUPABASE_TOKEN)
    data = supaclient.auth.sign_in_with_password({"email": username, "password": password})
    return data
