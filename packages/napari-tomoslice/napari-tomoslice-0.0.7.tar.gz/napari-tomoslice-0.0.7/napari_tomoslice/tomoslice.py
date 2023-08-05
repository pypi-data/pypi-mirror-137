from enum import auto
from functools import partial
from typing import Optional

import mrcfile
import napari
import napari.layers
import numpy as np
from napari.utils.misc import StringEnum
from psygnal import Signal

from .plane_controls import shift_plane_along_normal, set_plane_normal_axis, \
    orient_plane_perpendicular_to_camera, orient_plane_on_mouse_drag
from .points_controls import add_point
from napari.utils.geometry import clamp_point_to_bounding_box


class RenderingMode(StringEnum):
    VOLUME = auto()
    PLANE = auto()


class TomoSlice:
    plane_thickness_changed = Signal(float)
    rendering_mode_changed = Signal(str)

    def __init__(self, viewer: napari.Viewer):
        self.viewer = viewer
        self.viewer.dims.ndisplay = 3
        self.volume_layer: Optional[napari.layers.Image] = None
        self.bounding_box_layer: Optional[napari.layers.Points] = None
        self._rendering_mode: RenderingMode = RenderingMode.VOLUME

    @property
    def rendering_mode(self):
        return str(self._rendering_mode)

    @rendering_mode.setter
    def rendering_mode(self, value):
        self._rendering_mode = RenderingMode(value)
        self.volume_layer.experimental_slicing_plane.enabled = self._render_as_plane
        self.rendering_mode_changed.emit(self.rendering_mode)

    @property
    def _render_as_plane(self):
        if self.rendering_mode == RenderingMode.PLANE:
            return True
        else:
            return False

    @property
    def plane_thickness(self):
        return self.volume_layer.experimental_slicing_plane.thickness

    @plane_thickness.setter
    def plane_thickness(self, value):
        self.volume_layer.experimental_slicing_plane.thickness = value
        self.plane_thickness_changed.emit()

    def increase_plane_thickness(self, event=None):
        self.volume_layer.experimental_slicing_plane.thickness += 1
        self.plane_thickness_changed.emit()

    def decrease_plane_thickness(self, event=None):
        self.volume_layer.experimental_slicing_plane.thickness -= 1
        self.plane_thickness_changed.emit()

    def open_tomogram(self, tomogram_file: str):
        with mrcfile.open(tomogram_file) as mrc:
            tomogram = mrc.data
        self.add_volume_layer(tomogram)
        self.add_bounding_box()
        self.connect_callbacks()
        self.viewer.reset_view()
        self.viewer.camera.angles = (140, -55, -140)
        self.viewer.camera.zoom = 0.8
        self.viewer.layers.selection.active = self.volume_layer

    def close_tomogram(self):
        self.disconnect_callbacks()
        self.viewer.layers.remove(self.volume_layer)
        self.viewer.layers.remove(self.bounding_box_layer)

    def add_volume_layer(self, tomogram: np.ndarray):
        render_as_plane = True if self.rendering_mode == RenderingMode.PLANE else False
        plane_parameters = {
            'enabled': render_as_plane,
            'position': np.array(tomogram.shape) / 2,
            'normal': (1, 0, 0),
            'thickness': 5,
        }
        self.volume_layer = self.viewer.add_image(
            data=tomogram,
            name='tomogram',
            colormap='gray_r',
            rendering='mip',
            experimental_slicing_plane=plane_parameters,
        )

    def add_bounding_box(self):
        bounding_box_max = self.volume_layer.data.shape
        bounding_box_points = np.array(
            [
                [0, 0, 0],
                [0, 0, bounding_box_max[2]],
                [0, bounding_box_max[1], 0],
                [bounding_box_max[0], 0, 0],
                [bounding_box_max[0], bounding_box_max[1], 0],
                [bounding_box_max[0], 0, bounding_box_max[2]],
                [0, bounding_box_max[1], bounding_box_max[2]],
                [bounding_box_max[0], bounding_box_max[1], bounding_box_max[2]]
            ]
        )
        self.bounding_box_layer = self.viewer.add_points(
            data=bounding_box_points,
            name='bounding box',
            blending='opaque',
            face_color='cornflowerblue',
            edge_color='black',
            edge_width=2,
            size=10,
        )

    def activate_plane_follows_camera(self):
        self.viewer.mouse_drag_callbacks.append(
            self._plane_follows_camera_callback
        )

    def deactivate_plane_follows_camera(self):
        self.viewer.mouse_drag_callbacks.remove(
            self._plane_follows_camera_callback
        )

    def shift_plane_up(self, event=None):
        updated_position = \
            np.array(
                self.volume_layer.experimental_slicing_plane.position
            ) + 3 * np.array(
                self.volume_layer.experimental_slicing_plane.normal
            )
        self.volume_layer.experimental_slicing_plane.position = clamp_point_to_bounding_box(
            point=updated_position,
            bounding_box=self.volume_layer._display_bounding_box(
                self.viewer.dims.displayed)
        )

    def shift_plane_down(self, event=None):
        updated_position = \
            np.array(
                self.volume_layer.experimental_slicing_plane.position
            ) - 3 * np.array(
                self.volume_layer.experimental_slicing_plane.normal
            )
        self.volume_layer.experimental_slicing_plane.position = clamp_point_to_bounding_box(
            point=updated_position,
            bounding_box=self.volume_layer._display_bounding_box(
                self.viewer.dims.displayed)
        )

    def if_plane_enabled(self, func):
        """Decorator for conditional execution of callbacks.
        """

        def inner(*args, **kwargs):
            if self.volume_layer.experimental_slicing_plane.enabled and self.volume_layer.visible:
                return func(*args, **kwargs)

        return inner

    def connect_callbacks(self):
        # plane position (click and drag)
        self._shift_plane_callback = partial(
            self.if_plane_enabled(shift_plane_along_normal),
            layer=self.volume_layer
        )
        self.viewer.mouse_drag_callbacks.append(
            self._shift_plane_callback
        )

        # plane orientation (ortho)
        for key in 'xyz':
            callback = partial(
                self.if_plane_enabled(set_plane_normal_axis),
                layer=self.volume_layer,
                axis=key
            )
            self.viewer.bind_key(key, callback)

        #
        self.volume_layer.experimental_slicing_plane.events.enabled.connect(
            partial(self.rendering_mode_changed.emit, self.rendering_mode)
        )
        self.volume_layer.experimental_slicing_plane.events.thickness.connect(
            partial(self.plane_thickness_changed.emit, self.plane_thickness)
        )

        # # plane orientation(camera)
        # self._orient_plane_callback = partial(
        #     self.if_plane_enabled(orient_plane_perpendicular_to_camera),
        #     layer=self.volume_layer
        # )
        # self.viewer.bind_key('o', self._orient_plane_callback)

        # plane thickness (buttons)
        self.viewer.bind_key(
            '[', self.if_plane_enabled(self.decrease_plane_thickness)
        )
        self.viewer.bind_key(
            ']', self.if_plane_enabled(self.increase_plane_thickness)
        )

        # plane position (buttons)
        self.viewer.bind_key(
            'PageUp', self.if_plane_enabled(self.shift_plane_up)
        )
        self.viewer.bind_key(
            'PageDown', self.if_plane_enabled(self.shift_plane_down)
        )

        # create plane follows camera mouse callback
        self._plane_follows_camera_callback = partial(
            self.if_plane_enabled(orient_plane_on_mouse_drag),
            plane_layer=self.volume_layer
        )

        # plane orientation (oblique, on hold o)
        # this makes the plane follow the camera on keypress and stops on
        # key release
        @self.viewer.bind_key('o')
        def plane_orientation_toggle(viewer):
            orient_plane_perpendicular_to_camera(viewer, self.volume_layer)
            old_camera_center = np.copy(viewer.camera.center)
            old_camera_zoom = np.copy(viewer.camera.zoom)
            viewer.camera.center = \
                self.volume_layer.experimental_slicing_plane.position
            viewer.camera.zoom = 3 * old_camera_zoom
            self.viewer.mouse_drag_callbacks.remove(self._shift_plane_callback)
            self.activate_plane_follows_camera()
            yield
            self.deactivate_plane_follows_camera()
            self.viewer.mouse_drag_callbacks.append(self._shift_plane_callback)
            viewer.camera.center = old_camera_center
            viewer.camera.zoom = old_camera_zoom

        self._plane_orientation_toggle = plane_orientation_toggle

        # add point in points layer on alt-click
        self._add_point_callback = partial(
            self.if_plane_enabled(add_point),
            volume_layer=self.volume_layer
        )
        self.viewer.mouse_drag_callbacks.append(
            self._add_point_callback
        )

    def disconnect_callbacks(self):
        self.viewer.mouse_drag_callbacks.remove(self._shift_plane_callback)
        self.viewer.mouse_drag_callbacks.remove(self._add_point_callback)
        for key in 'xyzo[]':
            self.viewer.keymap.pop(key.upper())

