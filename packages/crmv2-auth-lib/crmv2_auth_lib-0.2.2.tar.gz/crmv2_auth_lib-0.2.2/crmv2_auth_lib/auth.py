from pydantic import BaseModel
from bson.objectid import ObjectId
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from fastapi.param_functions import Depends
from datetime import timedelta, datetime
from fastapi.security.oauth2 import SecurityScopes
from config import ENVIRONMENT, SECRET_KEY, ALGORITHM, BASEURL

import jwt


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=BASEURL+"crmv2/main_auth/auth/login"
)

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Sesi telah berakhir, silahkan login kembali!",
    headers={"WWW-Authenticate": "Bearer"},
)

ROLE_EXCPETION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Role tidak memiliki akses",
    headers={"WWW-Authenticate": "Bearer"},
)

ACCESS_TOKEN_EXPIRE_MINUTES = 15


# =============================class=============================
class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if type(v) == str:
            v = ObjectId(v)
        if not isinstance(v, ObjectId):
            raise ValueError("Not a valid ObjectId")
        return str(v)


class JwtToken(BaseModel):
    name: str = None
    username: str = None
    email: str = None
    schoolId: ObjectIdStr = None
    bankCentralId: ObjectIdStr = None
    bankAreaId: ObjectIdStr = None
    bankBranchId: ObjectIdStr = None
    userId : ObjectIdStr = None
    # teamAreaId: ObjectIdStr = None
    role : str = None
    exp : int = 1000

# =============================controller=============================
async def mytoken(token: str = Depends(oauth2_scheme)):
    return token

async def create_access_token(data: JwtToken, expires_delta: int, ALGORITHM='HS256'):
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=1)
    data.exp = expire
    encoded_jwt = jwt.encode(data.dict(), SECRET_KEY, ALGORITHM)

    return encoded_jwt

async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    try:
        # decode token and extract username and expires data
        idxSecret = len(security_scopes.scopes)-1
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        data_token = JwtToken()
        data_token.name = payload.get("name")
        data_token.username = payload.get("username")
        data_token.email = payload.get("email")
        data_token.exp = payload.get("exp")
        data_token.userId = payload.get("userId")
        data_token.schoolId = payload.get("schoolId")
        data_token.bankCentralId = payload.get("bankCentralId")
        data_token.bankAreaId = payload.get("bankAreaId")
        data_token.bankBranchId = payload.get("bankBranchId")
        # data_token.teamAreaId = payload.get("teamAreaId")

        data_token.role = payload.get("role")
        if str(security_scopes.scopes[0]).lower() == "*":
            print("Semua Role memiliki akases")
        elif str(data_token.role).upper() in str(security_scopes.scopes):
            print(f"Role {str(data_token.role).lower()} memiliki akases")
        elif str(data_token.role).upper() not in str(security_scopes.scopes):
            raise ROLE_EXCPETION
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION
    return data_token

async def create_refresh_token(response, token, ALGORITHM='HS256'):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data_token = JwtToken()
        data_token.name = payload.get("name")
        data_token.username = payload.get("username")
        data_token.email = payload.get("email")
        data_token.exp = payload.get("exp")
        data_token.userId = payload.get("userId")
        data_token.schoolId = payload.get("schoolId")
        data_token.bankCentralId = payload.get("bankCentralId")
        data_token.bankAreaId = payload.get("bankAreaId")
        data_token.bankBranchId = payload.get("bankBranchId")
        # data_token.teamAreaId = payload.get("teamAreaId")
        data_token.role = payload.get("role")
        # cek token sekarang masih on atau gak
        if datetime.utcfromtimestamp(payload.get("exp")) > datetime.utcnow():
            # cek username masih ada atau tidak
            # if(await GetUserOr404ByUsername(payload.get("username"))):
            access_token = await create_access_token(data_token, 15, SECRET_KEY)
            # print(access_token)
            btoken = "Bearer " + str(access_token)
            response.headers["Authorization"] = btoken
            return {"access_token": access_token}

    except Exception:
        raise CREDENTIALS_EXCEPTION
    raise CREDENTIALS_EXCEPTION

async def get_config():
    return {
        'env' : ENVIRONMENT,
        'alg' : ALGORITHM,
        'url' : BASEURL
    }
