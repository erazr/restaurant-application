from fastapi import FastAPI, Request, Form, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fastapi.responses import JSONResponse
#from starlette.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware,
                   secret_key="bebra228")

DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

Base = declarative_base()


def check_authentication(func):
    async def wrapper(request: Request, *args, **kwargs):
        if "user" not in request.session:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован.")
        return await func(request, *args, **kwargs)
    return wrapper


class UserRegistration(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserAction(BaseModel):
    action: str


class PostCreate(BaseModel):
    title: str
    content: str

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))  # Внешний ключ для связи с пользователем


Base.metadata.create_all(bind=engine)


@app.post("/register")
async def register(request: Request, user_data: UserRegistration):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        db.close()
        return JSONResponse(content={"detail": "Имя пользователя уже используется. Используйте другое."}, status_code=400)
    user = User(username=user_data.username, password=user_data.password)
    db.add(user)
    db.commit()
    db.close()
    return JSONResponse(content={"message": "Пользователь успешно зарегистрирован."})


@app.post("/login")
async def login(request: Request, user_data: UserLogin):
    db = SessionLocal()
    user = db.query(User).filter(User.username == user_data.username, User.password == user_data.password).first()
    db.close()
    if user:
        if "user" in request.session:
            raise HTTPException(status_code=400, detail="Пользователь уже авторизован.")
        request.session["user"] = user.id
        return {"message": "Пользователь авторизовался успешно."}
    else:
        #raise HTTPException(status_code=401, detail="Авторизация не прошла. Проверьте ваши данные.")
        return {"message": "Авторизация не прошла. Проверьте ваши данные."}


@app.post("/logout")
async def logout(request: Request, user_action: UserAction):
    if user_action.action == "logout":
        # Проверка, что пользователь аутентифицирован
        if "user" not in request.session:
            raise HTTPException(status_code=401, detail="Пользователь не авторизован.")

        # Удаление информации о пользователе из сессии
        del request.session["user"]

        return {"message": "Пользователь успешно вышел."}
    else:
        raise HTTPException(status_code=400, detail="Неверное действие. Ожидается 'logout'.")


@app.post("/create_post")
async def create_post(request: Request, post_data: PostCreate):
    # Проверьте, авторизован ли пользователь
    if "user" not in request.session:
        raise HTTPException(status_code=401, detail="Пользователь не авторизован.")

    db = SessionLocal()
    post = Post(title=post_data.title, content=post_data.content, user_id=request.session["user"])
    db.add(post)
    db.commit()
    db.close()
    return JSONResponse(content={"message": "Пост успешно создан."})
