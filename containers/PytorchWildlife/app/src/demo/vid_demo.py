# basic imports
from PIL import Image
from pathlib import Path
import numpy as np
import supervision as sv
import sqlite3


# storage for identified objects
class DB:
    def __init__(self) -> None:
        p = Path("/db/wildlife.db")
        self._db_path: str = p.resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        cnn = sqlite3.connect(self._db_path)
        c = cnn.cursor()
        stmt = '''create table if not exists idx_logs (vid_name text, frame_idx int, prediction text, confidence real)'''
        c.execute(stmt)

    def add_frame_classifications(self, vid_name: str, frame_index: int, classification: str, confidence: float):
        try:
            conn = sqlite3.connect(self._db_path)
            c = conn.cursor()
            c.execute(
                "INSERT INTO idx_logs (vid_name, frame_idx, prediction, confidence) VALUES (?, ?, ?, ?)", 
                (vid_name, frame_index, classification, confidence))
            conn.commit()
            conn.close()
        except Exception as e:
            print("Classification not saved to db")
            print("!"*50)
            print(e)
            return

# pytorch imports for tensor operations
import torch

# Importing the models, transformations, and utility functions from PytorchWildlife
from PytorchWildlife.models import detection as pw_detection
from PytorchWildlife.models import classification as pw_classification
from PytorchWildlife.data import transforms as pw_trans
from PytorchWildlife import utils as pw_utils

# Setting the device to use for computations
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
db = DB()

vid_path = Path("/vids")
processed_vid_path = vid_path / "processed"
processed_vid_path.mkdir(parents=True, exist_ok=True)

# Initialze models for detection and classification
detection_model = pw_detection.MegaDetectorV5(device=DEVICE, pretrained=True)
classification_model = pw_classification.AI4GAmazonRainforest(device=DEVICE, pretrained=True)

# Defining transformations for detection and classification
trans_det = pw_trans.MegaDetector_v5_Transform(target_size=detection_model.IMAGE_SIZE, 
                                               stride=detection_model.STRIDE)
trans_clf = pw_trans.Classification_Inference_Transform(target_size=224)

# Initializing a box annotator for visualizing detections
box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)

def callback(frame: np.ndarray, index: int) -> np.ndarray:
    results_det = detection_model.single_image_detection(trans_det(frame), frame.shape, index)
    labels = []

    for xyxy in results_det["detections"].xyxy:
        cropped_image = sv.crop_image(image=frame, xyxy=xyxy)
        results_clf = classification_model.single_image_classification(trans_clf(Image.fromarray(cropped_image)))
        labels.append("{} {:.2f}".format(results_clf["prediction"], results_clf["confidence"]))
        db.add_frame_classifications(vid_name=SOURCE_VID_PATH.split("/")[-1], frame_index=index, classification=results_clf["prediction"], confidence=results_clf["confidence"])
    
    annoted_frame = box_annotator.annotate(scene=frame, detections=results_det["detections"], labels=labels)

    print("-"*50)
    print(f"frame {index} processed")
    labels_msg = "\n".join(labels)
    print(f"labels: {labels_msg}")
    print("-"*50)
    print("\n")

    return annoted_frame

vids = [f for f in vid_path.iterdir() if f.is_file() and (f.suffix.lower() == ".mp4" or f.suffix.lower() == ".avi")]
for vid in vids:
    SOURCE_VID_PATH = str(vid.resolve())
    TARGET_VID_PATH = str((processed_vid_path / f"{vid.stem}_processed.mp4").resolve())
    pw_utils.process_video(SOURCE_VID_PATH, TARGET_VID_PATH, callback, target_fps=5)