from fastapi import FastAPI, responses, status
from pydantic import BaseModel, Field
from typing import Optional
from db import session_factory, User, UserGroup

app = FastAPI()


@app.get('/')
def homepage():
    """Домашняя страница"""
    return {"Hello": "ITCamp"}


@app.get('/groups')
def list_groups():
    """Список всех групп"""
    with session_factory() as session:
        return session.query(UserGroup).all()
    
    
@app.get('/users')
def list_users():
    """Список всех пользователей"""
    with session_factory() as session:
        return session.query(User).all()


@app.get('/greetings')
def greetings(person: str): # так указываются параметры, передаваемые в самом URL.
    # С помощью тайпхинта к person fastapi укажет этот тип в документации
    """Приветствие"""
    return {"Hello": f"{person}"}


# Если мы хотим послать параметры запроса в отдельном теле, необходимо воспользоватся pydantic

class RequestBody(BaseModel):
    first_name: str = Field(title="Имя")
    last_name: str = Field(title="Фамилия")
    email: str = Field(title="Электронная почта")
    password: str = Field(title="Пароль")
    group_id: Optional[int] = Field(title="Идентификатор группы")


@app.post('/signup')
def signup(request: RequestBody):
    """Регистрация пользователя"""
    with session_factory() as session:
        exists = session.query(User).where(User.email == request.email).all()
        if exists:
            return responses.Response(status_code=status.HTTP_409_CONFLICT)
        
        user = User(**request.dict())
        session.add(user)
        session.commit()
        
        return request
    
    
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)