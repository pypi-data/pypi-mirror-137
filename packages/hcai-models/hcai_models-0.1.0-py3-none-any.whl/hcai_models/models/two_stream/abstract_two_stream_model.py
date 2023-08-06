from hcai_models.core.abstract_multi_input_model import AbstractMultiInputModel
from hcai_models.core.abstract_multi_output_model import AbstractMultiOutputModel
from tensorflow import keras
from hcai_models.core.keras_model import KerasModel


class AbstractTwoStreamModel(
    AbstractMultiInputModel, AbstractMultiOutputModel, KerasModel
):
    """
    An abstract implementation for use cases where two models or streams are fit to different datasets,
    and normalization between certain model layers is included in training as a loss.
    It is Keras-based.
    """

    def _make_input(
        self, input_shape: tuple, use_resize: bool = False, input_name: str = "image"
    ):
        if use_resize:
            input = keras.Input(shape=(None, None, input_shape[2]), name=input_name)
            input_in = keras.layers.experimental.preprocessing.Resizing(
                height=input_shape[0], width=input_shape[1], interpolation="bilinear"
            )(input)
        else:
            input = keras.Input(shape=input_shape, name=input_name)
            input_in = input

        return input, input_in

    def _prefix_model(self, model, prefix: str):
        """
        The provided prefix is added to each layer of the keras model except the inputs, to allow for later combination
        :param model: any keras model
        :param prefix: the prefix applied
        :return: None
        """
        for i, layer in enumerate(model.layers):
            if i > 0:
                layer._name = prefix + layer.name

    def _make_distance_losses(self, model, prefixes: list):
        """
        Assuming a model with two identical streams or branches, a given loss is applied
        between layers of the same same within their models respective prefixed namespaces

        :param model: 2-streamed keras model
        :param prefixes: prefixes of the models two branches
        :return: None
        """
        losses = []

        loss_dict = self._get_loss_heads_by_layer()
        for block, layers in loss_dict.items():
            stream_src = model.get_layer(f"{prefixes[0]}{block}")
            if stream_src is None:
                raise ValueError(
                    f"unknown model layer {block} in the loss_heads definition. Check your implementation."
                )
            stream_src = stream_src.output
            stream_trg = model.get_layer(f"{prefixes[1]}{block}").output

            for i, layer in enumerate(layers):
                # actual comparison layer
                if i == len(layers) - 1:
                    losses.append(layer(stream_src, stream_trg))
                # transformations before comparison
                else:
                    stream_src = layer(stream_src)
                    stream_trg = layer(stream_trg)
        return losses

    def _get_loss_heads_by_layer(self) -> dict:
        """
        Returns: a dict of lists, specifying a loss head to attach to two equivalent layers in each model stream
        The dict keys specify layer names in the source model.

        The last layer provided must be a distance measure, which will be used as a loss in the model.

        If more than one layer is specified in the list, all layers but the last will be appended on both streams
        before any loss. This can be used for pooling, flattening or gradient manipulation

        Example:
            return {
                "layer_name": [keras.layers.Flatten(), MaximumMeanDiscrepancyLoss()]
            }

            this will result in the source and target variant of layer_name first being flattened, then compared via MMD
        """
        raise NotImplementedError()

    def _build_model(self):

        input_shape = self.input_shapes["image_source"]
        head_size_source = self.output_shapes["prediction_source"]
        head_size_target = self.output_shapes["prediction_target"]
        use_resize = True

        input_src, input_in_src = self._make_input(
            input_shape, use_resize, "image_source"
        )
        input_trg, input_in_trg = self._make_input(
            input_shape, use_resize, "image_target"
        )

        efficientnet_src = self._make_baseline_model(input_in_src)
        self._prefix_model(efficientnet_src, "src_")
        dense_src = keras.layers.Dense(
            units=head_size_source, activation="softmax", name="prediction_source"
        )(efficientnet_src.layers[-2].output)

        efficientnet_trg = self._make_baseline_model(input_in_trg)

        self._prefix_model(efficientnet_trg, "trg_")
        dense_trg = keras.layers.Dense(
            units=head_size_target, activation="softmax", name="prediction_target"
        )(efficientnet_trg.layers[-2].output)

        input_label_src = keras.Input(shape=(1), name="label_source")
        input_label_trg = keras.Input(shape=(1), name="label_target")

        model = keras.Model(
            inputs=[input_src, input_trg, input_label_src, input_label_trg],
            outputs=[dense_src, dense_trg],
        )

        # pick equivalent layers from models and add mmd losses
        losses = self._make_distance_losses(model=model, prefixes=["src_", "trg_"])

        # classification losses
        losses.append(
            keras.losses.SparseCategoricalCrossentropy()(input_label_src, dense_src)
        )
        losses.append(
            keras.losses.SparseCategoricalCrossentropy()(input_label_trg, dense_trg)
        )

        for loss in losses:
            model.add_loss(loss)

        model.compile(
            optimizer="adam",
            metrics={
                "prediction_source": "sparse_categorical_accuracy",
                "prediction_target": "sparse_categorical_accuracy",
            },
        )

        return model

    def _make_baseline_model(self, input_tensor):
        raise NotImplementedError()
