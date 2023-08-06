from hcai_models.core.abstract_model import Model


class ImageModel(Model):
    """
    Abstract base class for image models.
    Specifies specific functionality and default values of image models and ensures compatibility with the interface for external calls.
    """

    def __init__(self, *args, input_height=300, input_width=300, input_channels=3, **kwargs):

        self.in_height = input_height
        self.in_width = input_width
        self.n_channels = input_channels

        # Overwriting default parameters
        kwargs.setdefault("input_shape", (input_height, input_width, input_channels))
        assert len(kwargs["input_shape"]) == 3

        # Init parents
        super().__init__(*args, **kwargs)

    def get_input_width(self):
        return self.input_shape[0]

    def get_input_heigth(self):
        return self.input_shape[1]

    def get_n_channels(self):
        return self.input_shape[2]
