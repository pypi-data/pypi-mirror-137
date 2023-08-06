import cv2
import numpy as np
import tensorflow as tf


class BoundingBoxImageCrop:
    def __init__(self, output_dim=(256, 256)):
        self.output_dim = output_dim

    def __call__(self, image, bb, *args, **kwargs):

        return tf.py_function(
            func=self._internal_call,
            inp=[image, bb],
            Tout=tf.float32,
        )

    def _internal_call(self, image, bbox, *args, **kwargs):
        image = np.array(image)
        bbox = np.array(bbox)

        if bbox[-1] == 0.0:
            # face not found -> fall back to original image
            scale, center = 1.0, np.array([image.shape[1] / 2, image.shape[0] / 2])
        else:
            detected_face = bbox[0:4]
            scale, center = self.get_scale_center(detected_face)

        mat = self.get_transform(center, scale, self.output_dim)[:2]
        image = cv2.warpAffine(image, mat, self.output_dim)

        return np.array(image)

    def get_scale_center(self, bb):

        center = np.array([bb[2] - (bb[2] - bb[0]) / 2, bb[3] - (bb[3] - bb[1]) / 2])
        scale = (bb[2] - bb[0] + bb[3] - bb[1]) / 220.0

        return scale, center

    def get_transform(self, center, scale, res):
        # Generate transformation matrix

        h = 200 * scale
        t = np.zeros((3, 3))
        t[0, 0] = float(res[1]) / h
        t[1, 1] = float(res[0]) / h
        t[0, 2] = res[1] * (-float(center[0]) / h + 0.5)
        t[1, 2] = res[0] * (-float(center[1]) / h + 0.5)
        t[2, 2] = 1

        return t
