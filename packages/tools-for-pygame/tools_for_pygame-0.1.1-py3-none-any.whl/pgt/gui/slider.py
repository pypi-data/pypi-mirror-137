from abc import ABC

from pgt.constants import CC, BUTTON_CLICK, BUTTON_HOVER, BUTTON_NORMAL
from pgt.mathf import Pos, Size

from .button import Button
from .draggable import Draggable
from .surface_element import SurfaceElement


class SliderCursor(Button, Draggable):
    """
    SliderCursor(Button, Draggable)

    Type: class

    Description: this class should be used to create the cursor of the
        slider
    """
    pass


class _SliderBase(SurfaceElement, ABC):
    def __init__(self,
                 ruler: Button,
                 cursor: SliderCursor,
                 *args, **kwargs):
        kwargs["elements"] = [ruler, cursor]
        super().__init__(*args, **kwargs)
        transform_func = lambda x: x - self.ul
        self.ruler = ruler
        self.cursor = cursor

        self.ruler.func = None
        self.ruler.fargs = []
        self.ruler.fkwargs = {}
        self.ruler.transform_mouse_pos = transform_func

        self.cursor.func = None
        self.cursor.fargs = []
        self.cursor.fkwargs = {}
        self.cursor.transform_mouse_pos = transform_func
        self.cursor._pos_point = CC

    @property
    def value(self):
        return None

    def draw(self, *args, **kwargs):
        if self.hidden: return
        if self.ruler.button_clicked \
           and not self.cursor.dragging \
           and not self.cursor.hovered:
            self.cursor.dragging = True
            self.cursor.drag_point = Pos(0, 0)

        if self.cursor.dragging:
            self.cursor.force_state = BUTTON_CLICK
        elif self.ruler.hovered or self.cursor.hovered:
            self.cursor.force_state = BUTTON_HOVER
        else:
            self.cursor.force_state = BUTTON_NORMAL

        self._SurfaceElement__size = self.size
        super().draw(*args, **kwargs)


class HSlider(_SliderBase):
    """
    HSlider(_SliderBase)

    Type: class

    Description: horizontal slider that returns a value between 0 and 1

    Args:
        'ruler' (Button): the ruler where the cursor slides
        'cursor' (SliderCursor): the cursor that can be dragged around

    Attrs:
        'ruler' (Button): see 'ruler' in args
        'cursor' (SliderCursor): see 'cursor' in args
        'max_x' (int): the maximum x position of the cursor
        'value' (float): the value that the slider is set to, if changed
            the position of the slider is changed accordingly
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_size = Size(self.ruler.w, max(self.ruler.h, self.cursor.h))
        self.size = new_size
        self._SurfaceElement__size = new_size
        self.ruler.x = 0

        if self.ruler.h <= self.cursor.h:
            self.cursor.b_top = 0
            self.cursor.b_bottom = self.true_size.h
        else:
            self.cursor.b_top = (self.true_size.h - self.cursor.h) / 2
            self.cursor.b_bottom = (self.true_size.h + self.cursor.h) / 2
        self.cursor.b_left = 0
        self.cursor.b_right = self.ruler.w

        self.max_x = self.ruler.w - self.cursor.w

    @property
    def value(self):
        return self.cursor.l / self.max_x

    @value.setter
    def value(self, new_value):
        self.cursor.l = self.max_x * new_value

    def draw(self, *args, **kwargs):
        prev_val = self.value
        self.ruler.w = self.true_size.w
        self.max_x = self.ruler.w - self.cursor.w
        self.cursor.b_right = self.ruler.w
        if not self.cursor.dragging:
            self.value = prev_val
        super().draw(*args, **kwargs)


class VSlider(_SliderBase):
    """
    HSlider(_SliderBase)

    Type: class

    Description: vertical slider that returns a value between 0 and 1

    Args:
        'ruler' (Button): the ruler where the cursor slides
        'cursor' (SliderCursor): the cursor that can be dragged around

    Attrs:
        'ruler' (Button): see 'ruler' in args
        'cursor' (SliderCursor): see 'cursor' in args
        'max_y' (int): the maximum y position of the cursor
        'value' (float): the value that the slider is set to, if changed
            the position of the slider is changed accordingly
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_size = Size(max(self.ruler.w, self.cursor.w), self.ruler.h)
        self.size = new_size
        self._SurfaceElement__size = new_size
        self.ruler.y = 0

        if self.ruler.w <= self.cursor.w:
            self.cursor.b_left = 0
            self.cursor.b_right = self.true_size.w
        else:
            self.cursor.b_left = (self.true_size.w - self.cursor.w) / 2
            self.cursor.b_right = (self.true_size.w + self.cursor.w) / 2
        self.cursor.b_top = 0
        self.cursor.b_bottom = self.ruler.h

        self.max_y = self.ruler.h - self.cursor.h

    @property
    def value(self):
        return self.cursor.u / self.max_y

    @value.setter
    def value(self, new_value):
        self.cursor.u = self.max_y * new_value

    def draw(self, *args, **kwargs):
        prev_val = self.value
        self.ruler.h = self.true_size.h
        self.max_y = self.ruler.h - self.cursor.h
        self.cursor.b_bottom = self.ruler.h
        if not self.cursor.dragging:
            self.value = prev_val
        super().draw(*args, **kwargs)
