from fastapi import FastAPI, HTTPException
from backend import crud, schemas
import uvicorn

app = FastAPI(title="AI Wiki Quiz Generator - FastAPI")

@app.post("/generate", response_model=schemas.QuizRecordOut)
def generate_quiz(payload: schemas.GeneratePayload):
    url = payload.url
    try:
        rec = crud.process_url(url)
        return rec
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def history():
    return crud.list_history()

@app.get("/details/{record_id}", response_model=schemas.QuizRecordOut)
def details(record_id: int):
    rec = crud.get_record(record_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Record not found")
    return rec

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
