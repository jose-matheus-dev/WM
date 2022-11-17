from typing import Callable
from . import Win32 as W
from .TK import INHERIT, TkData, E
from .Win32 import c, ct, hWnd, s, wt
_ = [c, ct, s, wt, W]


class Path:
    """Returns the absolute path of a source folder that is in the file path"""

    def __init__(self, source: str = '\\', _=__file__) -> None:
        self.source = f'{_.rsplit(source, 1)[0]}{source}\\' if _.rfind(source) != -1 else _[:_.rfind('\\')] + '\\'

    def __call__(self, add_on: str = '') -> str:
        return self.source + add_on


class Call(TkData, INHERIT):
    settings = {
        'Debug': {'Info': True},
        'WM': {'Call': True, 'visible': True, 'title': True},
        'TK': {'Call': True, 'visible': True, 'mainloop': True},
        'Win32': {'Call': True, 'visible': True, 'mainloop': True}}
    szTitle, szWindowClass = 'WM', 'WM'
    data: dict[str, E.Any] = {
        'WM_GETMINMAXINFO': [(152, 152), (1381, 774)],  # 'WM_GETMINMAXINFO': [(-14, -41), (-15, -15)]
        'TK': {}, 'WM': {'title': szTitle}, 'Win32': {}
    }
    W: dict[str, list[E.Any | E.Label | E.Button | E.Frame] | E.Any]
    ICON = Path('WM', __file__)('images\\resize.ico')
    COLORS = {'bar': ['#1f1f1f', '#353535', '#e81123']}
    WndProc: Callable[..., int]
    hWnd: hWnd

    def __init__(self, name: str = '', *_: E.Any, **__: E.Any):
        if name:
            self.data[name] = self.__class__.__dict__[name]
        super(TkData, self).__init__(*_, **__)


class System(Call):
    Call = Call

    def __init__(self, name: str = '', *_: E.Any, **__: E.Any):
        super().__init__(name, *_, **__)
        print('System Called:', self.__class__.__name__) if self.settings['Debug']['Info'] else ...
