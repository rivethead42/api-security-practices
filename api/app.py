from fastapi import FastAPI
from routers import usersRoutes
from routers import authRoutes
from routers import healthRoutes
from routers import googleRoutes
from routers import sensitiveDataRoutes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(usersRoutes.router)
app.include_router(authRoutes.router)
app.include_router(healthRoutes.router)
app.include_router(googleRoutes.router)
app.include_router(sensitiveDataRoutes.router)