from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# ----------------- FastAPI Setup -----------------
app = FastAPI(title="Notes CRUD API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Serve React Frontend -----------------
# Point this to the folder where your React build files exist
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_frontend():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not built or missing"}

# ----------------- Database Setup -----------------
DATABASE_URL = "sqlite:///./notes.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True, index=True)
    writer = Column(String, nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------- Pydantic Schema -----------------
class NoteSchema(BaseModel):
    writer: str
    text: str

# ----------------- Routes -----------------
@app.get("/api/notes/")
def get_notes():
    db = SessionLocal()
    notes = db.query(Note).order_by(Note.created_at.desc()).all()
    db.close()
    return [
        {
            "id": n.id,
            "writer": n.writer,
            "text": n.text,
            "created_at": n.created_at.isoformat()
        }
        for n in notes
    ]

@app.post("/api/notes/")
def create_note(note: NoteSchema):
    db = SessionLocal()
    new_note = Note(writer=note.writer, text=note.text)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    db.close()
    return {
        "id": new_note.id,
        "writer": new_note.writer,
        "text": new_note.text,
        "created_at": new_note.created_at.isoformat()
    }

@app.delete("/api/notes/{note_id}/")
def delete_note(note_id: int):
    db = SessionLocal()
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        db.close()
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    db.close()
    return {"message": "Note deleted successfully"}

