import logging
from pathlib import Path
from typing import List

import numpy as np
import supervision as sv

# pytorch imports for tensor operations
import torch
from PIL import Image
from PytorchWildlife import utils as pw_utils
from PytorchWildlife.data import transforms as pw_trans
from PytorchWildlife.models import classification as pw_classification

# Importing the models, transformations, and utility functions from PytorchWildlife
from PytorchWildlife.models import detection as pw_detection

import crud as crud
import database as dbm
import storage as stg


def process_video(id: int, file_path: Path, storage: stg.Storage):
    logging.info(f"Starting background work on video: {file_path.name}")
    if not crud.update_video("processing", id):
        logging.error(f"Stopping work on video: {file_path.name} due to db error")
        file_path.unlink()
        return

    logging.info(f"Processing video: {file_path.name}")
    try:
        # _mock_work(id)
        result_vid = _vid_word(id, file_path)
        result_storage = storage.send_to_storage(result_vid)
        _ = crud.update_video("completed", id, result_storage)
        logging.info(f"Completed processing video: {file_path}")
        result_vid.unlink(missing_ok=True)
    except Exception as e:
        logging.error(f"Error processing video - {file_path.name}: \n{e}")
    finally:
        file_path.unlink(missing_ok=True)



DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def _vid_word(id: int, vid_path: Path) -> Path:
    detection_model = pw_detection.MegaDetectorV5(device=DEVICE, pretrained=True)
    classification_model = pw_classification.AI4GAmazonRainforest(
        device=DEVICE, pretrained=True
    )
    trans_det = pw_trans.MegaDetector_v5_Transform(
        target_size=detection_model.IMAGE_SIZE, stride=detection_model.STRIDE
    )
    trans_clf = pw_trans.Classification_Inference_Transform(target_size=224)
    box_annotator = sv.BoxAnnotator(thickness=4, text_thickness=4, text_scale=2)

    src_vid_path = str(vid_path.resolve())
    tgt_vid_path = str(vid_path.parent / f"processed_{vid_path.name}")
    animal_ids: List[dbm.ClassifiedAnimal] = []

    def callback(frame: np.ndarray, index: int) -> np.ndarray:
        results_det = detection_model.single_image_detection(
            trans_det(frame), frame.shape, index
        )
        labels = []
        for xyxy in results_det["detections"].xyxy:
            cropped_image = sv.crop_image(image=frame, xyxy=xyxy)
            results_clf = classification_model.single_image_classification(
                trans_clf(Image.fromarray(cropped_image))
            )
            labels.append(
                "{} {:.2f}".format(results_clf["prediction"], results_clf["confidence"])
            )
            animal_ids.append(
                dbm.ClassifiedAnimal(
                    video_id=id,
                    animal_name=results_clf["prediction"],
                    confidence=results_clf["confidence"],
                )
            )
        annoted_frame = box_annotator.annotate(
            scene=frame, detections=results_det["detections"], labels=labels
        )
        return annoted_frame

    pw_utils.process_video(src_vid_path, tgt_vid_path, callback, target_fps=10)
    crud.add_animal_classifications(animal_ids)
    return Path(tgt_vid_path)


def _mock_work(id: int):
    import random as rng

    animal_names = [
        "cat",
        "dog",
        "bird",
        "fish",
        "rabbit",
        "snake",
        "lizard",
        "hamster",
        "gerbil",
        "guinea pig",
    ]
    numbers = [5_000_000 + x for x in range(20)]
    for number in numbers:
        _ = sum([x for x in range(number)])
        animal = dbm.ClassifiedAnimal(
            video_id=id, animal_name=rng.choice(animal_names), confidence=rng.random()
        )
        _ = crud.add_animal_classification(animal)
