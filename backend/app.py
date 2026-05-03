from fastapi import FastAPI
from database import Base, engine
from routes import upload, violations

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(upload.router)
app.include_router(violations.router)

@app.get("/")
def root():
    return {"message": "Traffic Violation Backend Running"}