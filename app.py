from fastapi import FastAPI, status, Response, HTTPException
from db import session_factory, User, UserGroup
from models import SignUpRequest

app = FastAPI(
    title='SignUp macro-service',
    description='Presentation project for IT-camp 2022'
)


@app.get("/")
def read_root():
    with session_factory() as session, session.begin():
        greetings_to = session.query(User).first()
        return {"msg": f"{greetings_to.first_name} {greetings_to.last_name}"}


@app.get('/user/{user_id}')
def get_user_info_by_id(user_id: int):
    with session_factory() as session:
        q = session.query(
            User.first_name, User.last_name, UserGroup.name
        ).join(UserGroup).where(User.id == user_id).first()
        if q:
            first_name, last_name, name = q
            return {'first_name': first_name, 'last_name': last_name, 'group': name}
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@app.post('/users/signup')
def sign_up(data: SignUpRequest):
    with session_factory() as session:
        existing = session.query(User).where(User.email == data.email).all()
        if existing:
            raise HTTPException(status_code=409, detail='Email has already been registered')
        new = User(**data.dict())
        session.add(new)
        session.commit()


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, port=8001)