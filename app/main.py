from fastapi import FastAPI
from .database import Base, engine
from .routers import auth as auth_router, users as users_router, workouts as workouts_router, history as history_router
from fastapi.middleware.cors import CORSMiddleware

# create tables (for dev; in prod use migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="NXG FitTrack Backend")

origins = [
    "http://localhost:19006",   # Expo default
    "http://127.0.0.1:19006",
    "*",                        # Optional: allow all origins (dev only)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(users_router.router)
app.include_router(workouts_router.router)
app.include_router(history_router.router)
