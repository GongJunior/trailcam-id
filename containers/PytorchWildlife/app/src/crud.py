import logging
from typing import Union, List

from sqlalchemy.orm import Session

import database as dbm
from database import VideoProcess
from storage import LocalFile

initial_process_status = "received"


def was_previously_processed(
    file: LocalFile, db: Session
) -> Union[dbm.VideoProcess, None]:
    try:
        prev_record = (
            db.query(dbm.VideoProcess)
            .filter(dbm.VideoProcess.file_size == file.current_file.stat().st_size)
            .filter(dbm.VideoProcess.file_hash == file.file_hash)
            .first()
        )
        return prev_record
    except Exception as e:
        logging.error(f"Error checking if file was previously processed: {e}")
        return None


def add_new_video(file: LocalFile, db: Session) -> Union[VideoProcess, None]:
    try:
        db_vid = dbm.VideoProcess(
            batch_name=file._safe_batch_name,
            video_name=file._safe_file_name,
            status=initial_process_status,
            source_file=file.file_storage_path,
            file_hash=file.file_hash,
            file_size=file.current_file.stat().st_size,
        )
        db.add(db_vid)
        db.commit()
        db.refresh(db_vid)
        return db_vid
    except Exception as e:
        logging.error(f"Error adding new video to process: {e}")
        return None


def get_video(video_id: int, db: Session) -> Union[VideoProcess, None]:
    try:
        vid = db.query(dbm.VideoProcess).filter(dbm.VideoProcess.id == video_id).first()
        # include aggregation for any animals found
        return vid
    except Exception as e:
        logging.error(f"Error getting video info: {e}")
        return None


def update_video(status: str, id: int, completed_path: Union[str, None] = None) -> bool:
    try:
        with dbm.SessionLocal() as db:
            vid = db.query(dbm.VideoProcess).filter(dbm.VideoProcess.id == id).first()
            vid.status = status
            vid.processed_file = (
                completed_path if completed_path else vid.processed_file
            )
            db.commit()
        return True
    except Exception as e:
        logging.error(f"Error updating status is db: {e}")
        return False


def add_animal_classification(animal: dbm.ClassifiedAnimal) -> bool:
    try:
        with dbm.SessionLocal() as db:
            db.add(animal)
            db.commit()
        return True
    except Exception as e:
        logging.error(f"Error adding animal classification: {e}")
        return False


def add_animal_classifications(animals: List[dbm.ClassifiedAnimal]) -> bool:
    try:
        with dbm.SessionLocal() as db:
            db.add_all(animals)
            db.commit()
        return True
    except Exception as e:
        logging.error(f"Error adding animal classifications: {e}")
        return False
