from hcai_models.models.image.hcai_blaze_face.blaze_face import BlazeFace
import numpy as np
import tensorflow as tf


class BlazeFaceDetector:
    def __init__(self):
        self.blaze_face = BlazeFace(weights="ls3d-w", min_score_thres=0.7)
        self.blaze_face.build_model()

    def __call__(self, image, *args, **kwargs):
        return tf.py_function(func=self._internal_call, inp=[image], Tout=tf.float32)

    def _internal_call(self, image, *args, **kwargs):
        image = np.array(image)

        input_img, (xshift, yshift), orig_size = self.blaze_face.preprocessing(image)
        preds = self.blaze_face.predict(np.expand_dims(input_img, 0))
        detected_face = self.blaze_face.postprocessing(
            preds, shifts=(xshift, yshift), orig_size=orig_size
        )

        if detected_face.size == 0:
            # face not found -> none
            return np.array([0, 0, 0, 0, 0.0])
        else:
            return detected_face[0]
