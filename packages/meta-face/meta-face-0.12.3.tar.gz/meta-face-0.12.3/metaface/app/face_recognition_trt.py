import cv2
import numpy as np
from ..model_zoo import RetinaFaceTrt, ArcFaceTrt
from .common import Face


class FaceRecognitionTrt:
    def __init__(self, detection_model_path='../models/face_detection_fp16.trt',
                 recognition_model_path='../models/face_recognition_fp16.trt'):
        self.detector = RetinaFaceTrt(model_file=detection_model_path, input_size=(640, 480))
        self.recognizer = ArcFaceTrt(model_file=recognition_model_path)

    def predict(self, image):
        bboxes, kpss = self.detector.detect(image, max_num=0, metric='default')
        if bboxes.shape[0] == 0:
            return []
        faces = []
        for i in range(bboxes.shape[0]):
            bbox = bboxes[i, 0:4]
            det_score = bboxes[i, 4]
            kps = None
            if kpss is not None:
                kps = kpss[i]
            face = Face(bbox=bbox, kps=kps, det_score=det_score)
            self.recognizer.get(image, face)
            faces.append(face)
        return faces

    @staticmethod
    def compute_similarity(feature1, feature2):
        return np.sum(np.square(feature1 - feature2))

    def show(self, image, faces):
        img = image.copy()
        for face in faces:
            box = face.bbox.astype(int)
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
        return img
