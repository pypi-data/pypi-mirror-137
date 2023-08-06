from __future__ import division
import numpy as np
import os
import cv2
import tensorrt as trt
from ..utils import face_align
from ..utils import allocate_buffers, do_inference

__all__ = [
    'ArcFaceTrt',
]


class ArcFaceTrt:
    def __init__(self, model_file=None):
        assert model_file is not None
        self.model_file = model_file
        self.taskname = 'recognition'
        self.engine = self.get_model(model_file)
        self.context = self.engine.create_execution_context()
        self.inputs, self.outputs, self.bindings, self.stream = allocate_buffers(self.engine)
        self.input_shape = list(self.engine.get_binding_shape(self.engine[0]))
        self.output_shape = list(self.engine.get_binding_shape(self.engine[-1]))
        self.input_mean = 127.5
        self.input_std = 127.5

    def get_model(self, engine_file):
        if not os.path.exists(engine_file):
            FileNotFoundError('Trt file not exist')

        runtime = trt.Runtime(trt.Logger(trt.Logger.VERBOSE))
        with open(engine_file, "rb") as f:
            return runtime.deserialize_cuda_engine(f.read())

    def get(self, img, face):
        aimg = face_align.norm_crop(img, landmark=face.kps)
        face.embedding = self.get_feat(aimg).flatten()
        return face.embedding

    def compute_sim(self, feat1, feat2):
        from numpy.linalg import norm
        feat1 = feat1.ravel()
        feat2 = feat2.ravel()
        sim = np.dot(feat1, feat2) / (norm(feat1) * norm(feat2))
        return sim

    def get_feat(self, imgs):
        if not isinstance(imgs, list):
            imgs = [imgs]
        input_size = self.input_shape[2:]
        blob = cv2.dnn.blobFromImages(imgs, 1.0 / self.input_std, input_size,
                                      (self.input_mean, self.input_mean, self.input_mean), swapRB=True)
        image_batch_ravel = blob.ravel()
        np.copyto(dst=self.inputs[0].host, src=image_batch_ravel)
        net_out = do_inference(context=self.context,
                               bindings=self.bindings,
                               inputs=self.inputs,
                               outputs=self.outputs,
                               stream=self.stream,
                               batch_size=self.input_shape[0])
        return net_out[0]
