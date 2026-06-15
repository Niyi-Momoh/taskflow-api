from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users, items

app = FastAPI(
    title="FastAPI CRUD API",
    description="A demo CRUD API with JWT auth and PostgreSQL",
    version="1.0.0",
)

app.include_router(users.router)
app.include_router(items.router)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "FastAPI CRUD API", "docs": "/docs"}
