from fastapi import FastAPI
try:
    from .database import engine, Base
    from .routers import auth, todos, admin, users
except ImportError:
    from database import engine, Base
    from routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get('/ping')
async def ping():
    return {'pint': 'pong'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
