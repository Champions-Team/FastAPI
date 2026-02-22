from fastapi import FastAPI, HTTPException, Response, Depends
from  pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from authx import AuthX, AuthXConfig

import uvicorn


app = FastAPI()
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],  # Разрешаем наш HTML сервер
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserLoginSchema(BaseModel):
    username: str
    password: str



@app.post("/login")
def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401)


@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "top secret"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)