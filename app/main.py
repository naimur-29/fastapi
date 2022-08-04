from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ADDING CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins = [
        "*"
    ],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# ROUTES
@app.get("/")
def root():
    return {"message": "add '/docs' after the url to get the documentations!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)