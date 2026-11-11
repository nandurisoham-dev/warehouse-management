from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/packages")
def register_package(name, destination, weight, status="pending"):
    return functions.add_package(name=name, destination=destination, weight=weight, status=status)

@app.get("/packages/{id}")
def get_package(id):
    pkg = functions.get_package(id)
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg

@app.patch("/packages/{id}")
def update_package(id, name=None, destination=None, weight=None, status=None):
    pkg = functions.update_package(id=id, name=name, destination=destination, weight=weight, status=status)
    if not pkg:
        raise HTTPException(status_code=404, detail="Package not found")
    return pkg

@app.delete("/packages/{id}")
def delete_package(id):
    result = functions.delete_package(id)
    if result == "not_found":
        raise HTTPException(status_code=404, detail="Package not found")
    if result == "dispatched":
        raise HTTPException(status_code=400, detail="Cannot delete a dispatched package")
    return {"message": "Package deleted"}