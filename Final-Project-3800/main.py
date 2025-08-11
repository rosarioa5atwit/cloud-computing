from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from database import get_db_connection, get_db_cursor
import logging

app = FastAPI(title="Final Project API", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "API is running", "status": "ok"}

@app.get("/health")
async def health_check():
    """Database connectivity check"""
    try:
        with get_db_connection() as conn:
            cursor = get_db_cursor(conn)
            cursor.execute("SELECT 1")
            return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable")

@app.get("/api/test")
async def test_endpoint():
    """Simple test endpoint"""
    return {"test": "success", "data": [1, 2, 3]}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)