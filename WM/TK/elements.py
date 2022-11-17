import tkinter as tk
from tkinter import ttk
from typing import Any, Literal, Optional
from ..Win32 import hWnd


class Element:
    class __Save:
        _: list[Any]

        def __init__(self, *_: Any, **__: Any):
            super().__init__(*_, **__)
            getattr(self, '_', []).append(self)

    class Tk(__Save, tk.Tk):
        def __init__(self, *_: Any, **__: Any):
            super().__init__(*_, **__)
            self.wm_withdraw()
            super().after(5, self.__update)

        def __update(self):
            self.update_idletasks()
            self.hWnd = hWnd(self.wm_frame(), 16)

    class Style(__Save, ttk.Style):

        def map(self, style: str, query_opt: Any = None, **__: Any) -> dict[Any, Any]:
            return super().map(style, query_opt, **__)  # type: ignore

        def layout(self, style: str, layoutspec: Any = None) -> list[tuple[str, dict[str, Any]]]:
            return super().layout(style, layoutspec)  # type: ignore

        def configure(self, style: str, query_opt: Any = None, **__: Any) -> Any:
            return super().configure(style, query_opt, **__)  # type: ignore

    class Widget(__Save, ttk.Widget):

        def state(self, statespec: Optional[str] = None) -> tuple[str, ...]:
            return super().state(statespec)  # type: ignore

        def grid(self, row: int = 0, column: int = 0, sticky: str = 'nsew', **__: Any):  # type: ignore
            super().grid_configure(row=row, column=column, sticky=sticky, **__)

            def configure(weight: dict[int, tuple[int, int]] = {0: (1, 1)}):
                for i in weight:
                    self.rowconfigure(i, weight=weight[i][0])
                    self.columnconfigure(i, weight=weight[i][1])
                return self
            return configure

        def pack(self, fill: Literal['none', 'x', 'y', 'both'] = 'both', expand: int = 1, **__: Any):  # type: ignore
            super().pack(fill=fill, expand=expand, **__)

            def configure(weight: dict[int, tuple[int, int]] = {0: (1, 1)}):
                for i in weight:
                    self.rowconfigure(i, weight=weight[i][0])
                    self.columnconfigure(i, weight=weight[i][1])
                return self
            return configure

    class Frame(Widget, ttk.Frame):
        ...

    class Label(Widget, ttk.Label):
        ...

    class Button(Widget, ttk.Button):
        ...

    class Toplevel(__Save, tk.Toplevel):
        def __init__(self, *_: Any, **__: Any):
            super().__init__(*_, **__)
            self.wm_withdraw()
            super().after(5, self.__update)

        def __update(self):
            self.update_idletasks()
            self.hWnd = hWnd(self.wm_frame(), 16)

    class StringVar(__Save, tk.StringVar):
        ...

    class PhotoImage(__Save, tk.PhotoImage):
        def __generate(self, image: Optional[tk.PhotoImage]) -> tuple[tk.PhotoImage, Literal['copy'], tk.PhotoImage]:
            return (PhotoImage(), 'copy', self) if image is None else (self, 'copy', image)  # type: ignore

        def cropping(self, x1: int, y1: int, x2: int, y2: int, image: Optional[tk.PhotoImage] = None) -> tk.PhotoImage:
            self.tk.call(*self.__generate(image), '-from', x1, y1, x2, y2, '-to', 0, 0)
            return getattr(self, '_')[-1]


class Tk(Element.Tk):
    _: list[Element.Tk] = []


class Style(Element.Style):
    _: list[Element.Style] = []


class Frame(Element.Frame):
    _: list[Element.Frame] = []


class Label(Element.Label):
    _: list[Element.Label] = []


class Button(Element.Button):
    _: list[Element.Button] = []


class Toplevel(Element.Toplevel):
    _: list[Element.Toplevel] = []


class StringVar(Element.StringVar):
    _: list[Element.StringVar] = []


class PhotoImage(Element.PhotoImage):
    _: list[Element.PhotoImage] = []


Widget = Element.Widget
