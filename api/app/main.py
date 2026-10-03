from fastapi import FastAPI

from app.routes.leave import router as leave_router


app = FastAPI(title="AI Leave Assistant API", version="1.0.0")


app.include_router(leave_router)


@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Leave API is running"}
