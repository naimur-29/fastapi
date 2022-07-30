from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello ohh my api"}

@app.get("/posts")
def get_posts():
    return {"message": "message sent..."}