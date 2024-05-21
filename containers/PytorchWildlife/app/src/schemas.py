from datetime import datetime
from typing import Union

from pydantic import BaseModel, Field


class VideoProcessBase(BaseModel):
    batch_name: Union[str, None] = Field(
        default=datetime.today().strftime("%Y%m%d"),
        description="folder to group video files",
    )

    video_name: str = Field(description="name of video file")


class VideoProcessCreate(VideoProcessBase):
    pass


class VideoProcess(VideoProcessBase):
    id: int
    file_hash: str
    status: str
    source_file: str
    processed_file: Union[str, None] = None
    submit_time: Union[datetime, None] = None
    completed_time: Union[datetime, None] = None

    class Config:
        orm_mode = True
