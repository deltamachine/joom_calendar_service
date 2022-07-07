import secrets

from fastapi import FastAPI, HTTPException, status, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from core.routes import router
from core.settings import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
    allow_credentials=True
)

app.include_router(router)

security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, settings.swagger_user)
    correct_password = secrets.compare_digest(credentials.password, settings.swagger_password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password',
            headers={'WWW-Authenticate': 'Basic'}
        )
    return credentials.username


@app.get('/docs')
async def get_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url='/openapi.json', title='docs')


@app.get('/openapi.json')
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title='FastAPI', version='0.1.0', routes=app.routes)
