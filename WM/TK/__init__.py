"""Generated Tkinter Elements to Create a Custom Title Bar"""
from . import elements as E
from .elements import tk, ttk

_ = tk, ttk


class Type:
    def __class_getitem__(cls, item: str): return getattr(cls, item, False)

    def __init__(self, *_, **__: E.Any):
        super().__init__(*_, **__)


class Widget(Type):
    _ = Frame, Label, Button = E.Frame, E.Label, E.Button
    __ = {('Frame', 'Label', 'Button')[n]: element for n, element in enumerate((Frame._, Label._, Button._))}


class Inherit(Type):
    class Tk(E.Tk):
        ...

    class Style(E.Style):
        ...

    class Toplevel(E.Toplevel):
        ...
    __ = {('TK', 'Style', 'Toplevel')[n]: element._ for n, element in enumerate((Tk, Style, Toplevel))}


class Generate(Type):
    _ = Frame, Label, Button, StringVar, PhotoImage = E.Frame, E.Label, E.Button, E.StringVar, E.PhotoImage
    __: dict[str, list[E.Any]] = {element.__name__: element._ for element in _}

    def __class_getitem__(cls, item: str): return getattr(cls, item, False)


WIDGET = Widget
INHERIT = Inherit
GENERATE = Generate


class TkData:
    S: dict[str, list[E.Any]] = GENERATE.__ | INHERIT.__
    W = {n[0]: WIDGET.__[n] for n in WIDGET.__} | WIDGET.__
    data: dict[str, E.Any]

    class TK_(E.Tk):
        ...

    class WM_(E.Toplevel):
        ...
    TK: TK_
    WM: WM_

    def __class_getitem__(cls, name: str) -> E.Any: return {**cls.S | cls.W | cls.data | cls.__dict__}.get(name, False)

    def get(self, __key: str, __default: E.Any | bool = False): return self.__dict__.get(__key, __default)


if __name__ == '__main__':
    w = TkData.TK_()
    w.mainloop()
