import logging

from fastapi import (
    BackgroundTasks,
    Depends,
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Form,
)
from sqlalchemy.orm import Session

import crud as crud
import ptwservice as ptw
import schemas as schemas
from typing_extensions import Annotated
from database import Base, SessionLocal, engine
from storage import LocalFile, LocalStorage

Base.metadata.create_all(bind=engine)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
storage = LocalStorage()


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def service_test():
    return {"message": "Service Running"}


@app.post("/videoupload/", response_model=schemas.VideoProcess)
def upload_video(
    file: Annotated[UploadFile, File()],
    batch_name: Annotated[str, Form()],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    local_file = LocalFile(batch_name, file.filename, file.file)

    if not local_file.save_file_to_storage(storage):
        raise HTTPException(status_code=500, detail="Unable to save file to storage")

    prev_record = crud.was_previously_processed(local_file, db)
    if prev_record:
        local_file.current_file.unlink()
        msg = f"File already processed: {prev_record.id}"
        raise HTTPException(status_code=400, detail=msg)

    new_vid = crud.add_new_video(local_file, db)
    if not new_vid:
        local_file.current_file.unlink()
        raise HTTPException(status_code=500, detail="Unable to add file to process")
    background_tasks.add_task(ptw.process_video, new_vid.id, local_file.current_file, storage)
    return new_vid


@app.get("/videoupload/{video_id}", response_model=schemas.VideoProcess)
def get_video(video_id: int, db: Session = Depends(get_db)):
    vid = crud.get_video(video_id, db)
    if not vid:
        raise HTTPException(status_code=404, detail="Video not found")
    return vid
