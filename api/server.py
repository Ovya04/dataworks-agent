from fastapi import FastAPI, HTTPException
from api.handlers import execute_task, read_file

app = FastAPI()

@app.post("/run")
async def run_task(task: str):
    try:
        result = execute_task(task)
        return {"status": "success", "message": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file_api(path: str):
    return read_file(path)
