import hashlib
import html
import logging
import shutil
import uuid
from pathlib import Path
from typing import BinaryIO

uploaded_files_path = Path("/uploadedFiles")
if not uploaded_files_path.exists():
    uploaded_files_path.mkdir()

local_storage_path = Path("/localStorage")
if not local_storage_path.exists():
    local_storage_path.mkdir()


# implement a storage solution
# needs to accomplish the following:
# storage path should be accessable to user
# do not user paths in this container
# ideas:
# - azure blob storage
# - run an sftp container
class Storage:
    def __init__(self) -> None:
        pass

    def send_to_storage(self, file: Path) -> str:
        pass


class LocalStorage:
    def __init__(self) -> None:
        self.storage_path = local_storage_path

    def send_to_storage(self, file: Path) -> str:
        batch_folder = self.storage_path / file.parent.name
        new_file_path = batch_folder / f"{uuid.uuid4()}_{file.name}"
        if not batch_folder.exists():
            batch_folder.mkdir()
        try:
            shutil.copy(file, new_file_path)
            return str(new_file_path.resolve())
        except Exception as e:
            logging.error(f"Error sending file to storage: {e}")
            raise e


class LocalFile:
    def __init__(self, batch_name: str, file_name: str, file_data: BinaryIO) -> None:
        self._safe_batch_name = html.escape(batch_name).replace("/", "")
        self._safe_file_name = html.escape(file_name).replace("/", "")
        self.rel_file_path = f"{self._safe_batch_name}/{self._safe_file_name}"
        self.current_file = uploaded_files_path / self.rel_file_path
        self._save_file_locally(file_data)
        self.file_hash = self._get_file_hash()
        self.file_storage_path = ""

    def _save_file_locally(self, file_data: BinaryIO) -> bool:
        self.current_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.current_file, "wb") as buffer:
                buffer.write(file_data.read())
            return True
        except Exception as e:
            logging.error(f"Error saving file: {e}")
            return False

    def save_file_to_storage(self, storage: Storage) -> bool:
        try:
            self.file_storage_path = storage.send_to_storage(self.current_file)
            return True
        except Exception as e:
            self.current_file.unlink()
            logging.error(f"Error sending file to storage: {e}")
            return False

    def _get_file_hash(self) -> str:
        algo = "md5"
        try:
            with open(self.current_file, "rb") as buffer:
                m = hashlib.md5()
                while chunk := buffer.read(8192):
                    m.update(chunk)
                hash_val = m.hexdigest()
                return f"{algo}:{hash_val}"
        except Exception as e:
            logging.error(f"Error hashing file: {e}")
            return f"{algo}:error"
