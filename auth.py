from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi import HTTPException,status,Depends


security = HTTPBasic()


def authorize_user(credentials : HTTPBasicCredentials = Depends(security)):
    if credentials.username == 'testuser' and credentials.password == 'testpw':
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User Unauthorized"
        )
