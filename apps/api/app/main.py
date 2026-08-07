from fastapi import FastAPI

app = FastAPI(
    title="AI Investment Intelligence Platform API",
    description="Backend API for AIIP Technologies",
    version="0.1.0-alpha.2",
)


@app.get("/")
async def root():
    return {
        "company": "AIIP Technologies",
        "product": "AI Investment Intelligence Platform",
        "platform": "AIIP",
        "status": "running",
        "version": "0.1.0-alpha.2",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }