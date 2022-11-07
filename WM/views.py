from .core import Call, System
from .TK import GENERATE, E


class Element(E.Widget, E.PhotoImage, System, Call):  # type: ignore
    def __new__(cls, name: str = '', *_: E.Any, generic: bool = False, **__: E.Any):
        E = GENERATE.__dict__[name](*_, **__)
        if generic:
            del E._[-1]
        return E


class Generate(System, Call):
    StringVar = GENERATE.StringVar._

    def __init__(self, ):
        self.WM.columnconfigure(0, weight=1)
        Element('Frame', self.WM).grid(ipady=1)({0: (1, 1)})
        Element('Label', self.W['F'][-1], textvar=Element('StringVar')).grid(pady=(0, 3))
        self.StringVar[0].set(self.data['WM']['title']) if self.data['WM'].get('title', False) else ...
        Element('Button', self.W['F'][-1]).grid(0, 3, pady=1)
        Element('Button', self.W['F'][-1]).grid(0, 4, pady=1)
        Element('Button', self.W['F'][-1]).grid(0, 5, pady=1)


class Views(System, Call):
    def __init__(self):
        super().__init__()
        Generate()
