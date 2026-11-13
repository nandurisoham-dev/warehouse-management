from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions
from fastapi import Header

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/packages")
def register_package(name, destination, weight, status="pending", token = Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail = "Invalid or expired token")
    return functions.add_package(name=name, destination=destination, weight=weight, status=status)

@app.get("/packages/{id}")
def get_package(id, token = Header(None)):
    pkg = functions.get_package(id)
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code = 401, detail="Invalid or expired token")
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg

@app.patch("/packages/{id}")
def update_package(id, name=None, destination=None, weight=None, status=None, token = Header(None)):
    pkg = functions.update_package(id=id, name=name, destination=destination, weight=weight, status=status)
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code = 401, detail="Invalid or expired token")
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg

@app.delete("/packages/{id}")
def delete_package(id, token = Header(None)):
    result = functions.delete_package(id)
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code = 401, detail="Invalid or expired token")
    if result == "not_found":
        raise HTTPException(status_code=404, detail="Package not found")
    if result == "dispatched":
        raise HTTPException(status_code=400, detail="Cannot delete a dispatched package")
    return {"message": "Package deleted"}

@app.post("/login")
def login(username:str, password:str):
    token = functions.verify_login(username=username, password=password)
    if token is None:
        raise HTTPException(status_code=401, detail="invalid username or password")
    return token

@app.post("/refresh")
def refresh(refresh_token = Header(None)):
    username = functions.verify_token(token=refresh_token, token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = functions.create_token(username=username, token_type="access")
    return {"access_token": access_token}

@app.get("/packages")
def search_packages(destination=None, status=None, arrival_date=None, token=Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_packages(destination=destination, status=status, arrival_date=arrival_date)

@app.get("/analytics")
def warehouse_analytics(token=Header(None)):
    username = functions.verify_token(token=token, token_type="access")
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_warehouse_analytics()