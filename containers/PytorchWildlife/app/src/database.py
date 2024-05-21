from pathlib import Path

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func

engine = create_engine(
    "sqlite:////db/wildlife.db", connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class VideoProcess(Base):
    __tablename__ = "video_process"
    id = Column(Integer, primary_key=True, index=True)
    batch_name = Column(String, nullable=False)
    video_name = Column(String, nullable=False)
    submit_time = Column(DateTime(timezone=True), server_default=func.now())
    completed_time = Column(DateTime(timezone=True), onupdate=func.now())
    status = Column(String, nullable=False)
    source_file = Column(String, nullable=False)
    processed_file = Column(String)
    file_hash = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    classifications = relationship("ClassifiedAnimal", back_populates="video_process")


class ClassifiedAnimal(Base):
    __tablename__ = "classified_animal"
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey("video_process.id"), nullable=False)
    animal_name = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    video_process = relationship("VideoProcess", back_populates="classifications")

class ClassNameMap(Base):
    __tablename__ = "class_name_map"
    id = Column(Integer, primary_key=True, index=True)
    classifier_name = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    display_description = Column(String, nullable=False)
