"""Centroids layer"""
import typing as ty

import numpy as np
from napari._vispy.layers.base import VispyBaseLayer
from vispy.scene.visuals import Line as LineVisual

if ty.TYPE_CHECKING:
    from ...layers import Centroids


def make_centroids(data: np.ndarray, orientation: str) -> np.ndarray:
    """Make centroids data in the format [[x, 0], [x, y]]"""
    array = np.zeros((len(data) * 2, 2), dtype=data.dtype)
    # in horizontal centroids, the three columns correspond to x-min, x-max, y
    if orientation == "horizontal":
        array[:, 1] = np.repeat(data[:, 0], 2)
        array[1::2, 0] = data[:, 1]
        array[0::2, 0] = data[:, 2]
    # in vertical centroids, the three columns correspond to x, y-min, y-max
    else:
        array[:, 0] = np.repeat(data[:, 0], 2)
        array[1::2, 1] = data[:, 1]
        array[0::2, 1] = data[:, 2]
    return array


class VispyCentroidsLayer(VispyBaseLayer):
    """Centroids layer"""

    def __init__(self, layer: "Centroids"):
        node = LineVisual()
        super().__init__(layer, node)

        self.layer.events.color.connect(self._on_appearance_change)
        self.layer.events.width.connect(self._on_appearance_change)
        self.layer.events.method.connect(self._on_method_change)
        self.layer.events.highlight.connect(self._on_highlight_change)

        self.reset()
        self._on_data_change()

    def _on_highlight_change(self, _event=None):
        """Mark region of interest on the visual"""

    def _on_appearance_change(self, _event=None):
        """Change the appearance of the data"""
        self.node.set_data(color=self.layer.color, width=self.layer.width)

    def _on_data_change(self, _event=None):
        """Set data"""
        self.node.set_data(
            make_centroids(self.layer.data, self.layer.orientation),
            connect="segments",
            color=self.layer.color,
            width=self.layer.width,
        )

    def _on_method_change(self, _event=None):
        self.node.method = self.layer.method
