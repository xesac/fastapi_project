from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, EmailStr



app = FastAPI()

class User(BaseModel):
    username: str
    age: int 
    email: EmailStr
    description: str | None = None
    address: str | None = None

lst = []


@app.get("/", response_model_exclude_unset=True)
async def get_portal():
    return lst

@app.post('/add/user/')
async def add_user(user: User) -> User:
    lst.append(user)
    return user