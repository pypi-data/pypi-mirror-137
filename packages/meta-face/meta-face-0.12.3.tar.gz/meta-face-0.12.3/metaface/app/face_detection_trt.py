import cv2
from ..model_zoo import RetinaFaceTrt


class FaceDetectionTrT:
    def __init__(self, model_path='../models/face_detection_fp16.trt', input_size=(640, 480)):
        self.detector = RetinaFaceTrt(model_file=model_path, input_size=input_size)

    def predict(self, image):
        boxes, _ = self.detector.detect(image)
        return boxes.astype(int)

    def show(self, image, boxes):
        img = image.copy()
        for box in boxes:
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
        return img

