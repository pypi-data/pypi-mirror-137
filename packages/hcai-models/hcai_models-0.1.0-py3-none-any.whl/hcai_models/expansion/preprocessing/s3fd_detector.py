import numpy as np
import torch
import tensorflow as tf

from hcai_models.models.image.hcai_sfd.sfd import S3FD


class S3FDDetector:
    def __init__(self):
        self.s3fd = S3FD(weights="ls3d-w", min_score_thres=0.8)
        self.s3fd._device = torch.device("cpu")
        self.s3fd.build_model()

    def __call__(self, image, *args, **kwargs):
        return tf.py_function(func=self._internal_call, inp=[image], Tout=tf.float32)

    def _internal_call(self, image, *args, **kwargs):
        image = np.array(image)

        input_img = self.s3fd.preprocessing(image)
        preds = self.s3fd.predict(np.expand_dims(input_img, 0))
        detected_face = np.array(preds)

        if detected_face.size == 0:
            # face not found -> none
            return np.array([0, 0, 0, 0, 0.0])
        else:
            return detected_face[0]
