import tensorflow as tf
import tensorflow_hub as hub
from tfhub_esrgan_wrapper.imgFunc import preprocess_image, plot_image
from tfhub_esrgan_wrapper.tensorFnc import gridify_tensor, tensorfy_grid


class ESRGAN:
    def __init__(self):
        self.hub_module = hub.load("https://tfhub.dev/captain-pool/esrgan-tf2/1")
        self.low_res_image = []

    def load_image(self, low_res_image):
        self.low_res_image = preprocess_image(low_res_image)

    def evaluate(self, plot_onoff=False):
        original_shape = self.low_res_image.shape
        tensor_grid, grid_structure = gridify_tensor(self.low_res_image)
        high_res_grid = []
        for tensor in tensor_grid:
            high_res_tensor = self.hub_module(tensor)
            high_res_grid.append(high_res_tensor)
        high_res_tensor = tensorfy_grid(high_res_grid, grid_structure, tuple([4 * x for x in original_shape]))

        if plot_onoff:
            plot_image(tf.squeeze(high_res_tensor))

        return tf.squeeze(high_res_tensor)
