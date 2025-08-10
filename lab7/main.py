from fastapi import FastAPI, Request, Response, HTTPException
from fastapi import Cookie
from fastapi import Header
from typing import Optional
import time
import hashlib

app = FastAPI(title="Headers and Cookies Lab", description="Lab 7: Service exercising headers and cookies")

user_sessions = {}
api_usage = {}
user_database = {"admin": "password"}  # Simple user storage

@app.get("/")
async def read_root(request: Request):
    return {
        "message": "Welcome to the FastAPI Headers and Cookies Lab!", 
        "available_routes": [
            "/signup", "/login", "/users/", "/profile/", "/api/secure", "/preferences", "/logout"
        ],
        "total_routes": 7
    }

@app.post("/signup")
async def signup(
    response: Response,
    username: str,
    password: str,
    user_agent: Optional[str] = Header(None),
    x_forwarded_for: Optional[str] = Header(None)
):
    if username in user_database:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    
    user_database[username] = password
    
    session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
    user_sessions[session_id] = {
        "username": username,
        "login_time": time.time(),
        "signup_ip": x_forwarded_for or "unknown"
    }
    
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
    response.set_cookie(key="username", value=username, max_age=3600)
    response.set_cookie(key="welcome_user", value="true", max_age=300)
    
    response.headers["X-Account-Created"] = "true"
    response.headers["X-User-Count"] = str(len(user_database))
    
    return {
        "message": "Account created successfully",
        "username": username,
        "session_id": session_id,
        "user_agent": user_agent,
        "signup_ip": x_forwarded_for or "unknown"
    }

@app.get("/login")
async def login(
    response: Response,
    username: str,
    password: str,
    user_agent: Optional[str] = Header(None)
):
    if username in user_database and user_database[username] == password:
        session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
        user_sessions[session_id] = {"username": username, "login_time": time.time()}
        
        response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
        response.set_cookie(key="username", value=username, max_age=3600)
        response.set_cookie(key="login_time", value=str(int(time.time())), max_age=3600)
        
        return {
            "message": "Login successful",
            "session_id": session_id,
            "user_agent": user_agent,
            "expires_in": "1 hour"
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/users/")
async def read_users(
    session_id: str = Cookie(None),
    username: str = Cookie(None),
    authorization: Optional[str] = Header(None)
):
    if session_id and session_id in user_sessions:
        return {
            "message": "User data retrieved via session cookie",
            "username": username,
            "session_valid": True,
            "auth_method": "cookie"
        }
    
    if authorization and authorization == "Bearer valid-token":
        return {
            "message": "User data retrieved via authorization header",
            "session_valid": False,
            "auth_method": "header"
        }
    
    raise HTTPException(status_code=401, detail="Authentication required")

@app.get("/profile/")
async def read_profile(
    response: Response,
    user_id: str | None = Header(default=None),
    session_id: str | None = Cookie(default=None),
    x_request_id: str | None = Header(default=None),
    accept_language: str | None = Header(default="en")
):
    if not session_id or session_id not in user_sessions:
        raise HTTPException(status_code=401, detail="Valid session required")
    
    response.headers["X-Response-Time"] = str(int(time.time()))
    response.headers["X-User-ID"] = user_id or "unknown"
    
    response.set_cookie(key="last_access", value=str(int(time.time())), max_age=3600)
    
    return {
        "message": "Profile data",
        "user_id": user_id,
        "session_id": session_id,
        "request_id": x_request_id,
        "language": accept_language,
        "session_user": user_sessions[session_id]["username"]
    }

@app.get("/api/secure")
async def secure_api(
    request: Request,
    response: Response,
    x_api_key: str = Header(...),
    x_client_version: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None)
):

    valid_keys = ["admin-key-123", "user-key-456"]
    if x_api_key not in valid_keys:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in api_usage:
        api_usage[client_ip] = []
    
    api_usage[client_ip] = [t for t in api_usage[client_ip] if current_time - t < 60]
    
    if len(api_usage[client_ip]) >= 20:
        response.headers["X-Rate-Limit-Exceeded"] = "true"
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    api_usage[client_ip].append(current_time)

    response.headers["X-Rate-Limit-Limit"] = "20"
    response.headers["X-Rate-Limit-Remaining"] = str(20 - len(api_usage[client_ip]))
    response.headers["X-Rate-Limit-Reset"] = str(int(current_time + 60))
    
    return {
        "message": "Secure API data",
        "api_key": x_api_key,
        "client_version": x_client_version,
        "user_agent": user_agent,
        "requests_remaining": 10 - len(api_usage[client_ip])
    }

@app.post("/preferences")
async def set_preferences(
    response: Response,
    language: str = "en",
    timezone: str = "UTC",
    session_id: str = Cookie(None)
):
    if not session_id or session_id not in user_sessions:
        raise HTTPException(status_code=401, detail="Valid session required")
    
    response.set_cookie(key="language", value=language, max_age=86400*30)
    response.set_cookie(key="timezone", value=timezone, max_age=86400*30)
    
    return {
        "message": "Preferences updated",
        "preferences": {
            "language": language,
            "timezone": timezone
        }
    }

@app.get("/preferences")
async def get_preferences(
    language: str = Cookie("en"),
    timezone: str = Cookie("UTC"),
    session_id: str = Cookie(None)
):
    return {
        "message": "Current preferences",
        "preferences": {
            "language": language,
            "timezone": timezone
        },
        "authenticated": session_id is not None and session_id in user_sessions
    }


@app.post("/logout")
async def logout(
    response: Response,
    session_id: str = Cookie(None)
):
    if session_id and session_id in user_sessions:
        del user_sessions[session_id]
    
    response.delete_cookie("session_id")
    response.delete_cookie("username")
    response.delete_cookie("login_time")
    response.delete_cookie("last_access")
    response.delete_cookie("language")
    response.delete_cookie("timezone")
    response.delete_cookie("welcome_user")
    
    return {"message": "Logged out successfully"}


if __name__ == "__main__":
    import uvicorn
    print("Server is running at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
    import uvicorn
    print("Server is running at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
