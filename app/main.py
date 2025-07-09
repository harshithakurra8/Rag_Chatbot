from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.document_handler import init_qdrant_collection, upload_document
from app.rag_pipeline import answer_question

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

@app.on_event("startup")
def startup():
    init_qdrant_collection()

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    return upload_document(file)

@app.post("/query/")
async def query(input: QueryRequest):
    return {"answer": answer_question(input.question)}
