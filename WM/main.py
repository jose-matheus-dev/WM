import re
from typing import Any, Optional, Callable

from .core import Call, System, W, c, ct, s, wt, hWnd
from .event import Event, WndProc
from .style import Style
from .views import Views

setattr(Call, 'dwStyle', c.WS_OVERLAPPEDWINDOW | c.WS_CLIPCHILDREN | c.WS_CLIPSIBLINGS | c.WS_VISIBLE)
setattr(Call, 'dwExStyle', c.WS_EX_LAYERED | c.WS_EX_APPWINDOW | c.WS_EX_ACCEPTFILES)  # | c.WS_EX_TOPMOST


class WinMain(System):
    """Win32API, an implementation of a Win32 window, to disable the normal title bar but keep resizing."""

    def __init__(self, *_: int, **__: int): super().__init__('hWnd', **__)

    def __new__(cls, w: int = 0, h: int = 0, x: int = 50, y: int = 0):
        W.user32.LoadStringW(W.hInst, 109, cls.szWindowClass, c.MAX_LOADSTRING)
        W.user32.LoadStringW(W.hInst, c.IDS_APP_TITLE, cls.szTitle, c.MAX_LOADSTRING)
        dwExStyle, atom, dwStyle = getattr(cls, 'dwExStyle'), cls.resister_class(), getattr(cls, 'dwStyle')
        cls.hWnd = W.user32.CreateWindowExW(dwExStyle, atom, cls.szTitle, dwStyle, x, y, w, h, 0, 0, W.hInst, 0)
        return super().__new__(cls)

    @classmethod
    def resister_class(cls):
        wcex = s.WNDCLASSEXW()
        wcex.cbSize = ct.sizeof(s.WNDCLASSEXW)
        wcex.style = c.CS_HREDRAW | c.CS_VREDRAW
        wcex.lpfnWndProc = getattr(cls, 'WndProc', WndProc)
        wcex.lpszClassName = cls.szWindowClass
        wcex.hInstance = W.hInst
        wcex.hIcon = W.user32.LoadImageW(W.hInst, cls.ICON, c.IMAGE_ICON, 0, 0, c.LR_DEFAULTSIZE | c.LR_LOADFROMFILE)
        wcex.hCursor = W.user32.LoadCursorW(0, c.IDC_ARROW)
        wcex.hbrBackground = W.gdi32.CreateSolidBrush(0x1F1F1F)
        return W.user32.RegisterClassExW(ct.byref(wcex))

    def mainloop(self):
        """A Win32API message loop"""
        if self.settings['Win32']['visible']:
            W.user32.SetLayeredWindowAttributes(self.hWnd, 255, 255, c.LWA_ALPHA)
        if self.settings['Win32']['mainloop']:
            msg = wt.MSG()
            hAccelTable = W.user32.LoadAcceleratorsW(W.hInst, 109)
            while W.user32.GetMessageW(ct.byref(msg), None, 0, 0):
                if not W.user32.TranslateAcceleratorW(msg.hWnd, hAccelTable, ct.byref(msg)):
                    W.user32.TranslateMessage(ct.byref(msg))
                    W.user32.DispatchMessageW(ct.byref(msg))


class WM(System, Call.WM_):
    hWnd: hWnd

    def __call__(self, *_: Any): return [i() for i in _]

    def __init__(self, *_):
        Call.WM = self.WM = self
        super().__init__()
        self.config(bg='#000001')
        self.attributes('-transparentcolor', '#000001')  # type: ignore

    def state(self, newstate: Optional[str] = None):  # type: ignore
        state = {'iconic': c.SW_MINIMIZE, 'zoomed': c.SW_MAXIMIZE, 'normal': c.SW_NORMAL}
        if newstate in ('iconic', 'zoomed', 'normal'):
            W.user32.ShowWindow(Call.hWnd, state.get(newstate))
        elif newstate is not None:
            raise ValueError(f'{newstate} is not an accepted state.')
        lpwndpl = s.WINDOWPLACEMENT()
        W.user32.GetWindowPlacement(Call.hWnd, ct.byref(lpwndpl))
        return {c.SW_MINIMIZE: 'iconic', c.SW_MAXIMIZE: 'zoomed', c.SW_NORMAL: 'normal'}.get(lpwndpl.showCmd, 'normal')


class Merge(System):
    def __init__(self):
        super().__init__()

        if self.settings['WM']['Call']:
            WM()(Views, Style, Event)

        if self.settings['Win32']['Call']:
            Call.hWnd = WinMain(334, 477).hWnd  # Create a Win32 Window Handler on System. 334x510
            self.WM.after(5, self.__settings) if self.settings['WM']['Call'] else ...

        self.TK.event_generate('<<Activate>>')
        self.TK.geometry('320x470+0+0')

    def __settings(self):
        W.user32.SetWindowLongPtrW(Call['TK'].hWnd, c.GWL_STYLE, c.WS_CHILD | c.WS_VISIBLE)
        W.user32.SetWindowLongPtrW(Call['WM'].hWnd, c.GWL_STYLE, c.WS_CHILD | c.WS_VISIBLE)  # c.WS_BORDER |
        W.user32.SetWindowLongPtrW(Call['WM'].hWnd, c.GWL_EXSTYLE, c.WS_EX_NOREDIRECTIONBITMAP)
        W.user32.SetParent(Call['WM'].hWnd, Call['hWnd'])
        W.user32.SetParent(Call['TK'].hWnd, Call['WM'].hWnd)


class TK(Merge, Call.TK_):
    def __call__(self, *_: Any): return [i() for i in _]

    def __init__(self):
        Call.TK = self.TK = self
        super().__init__()
        self['bg'] = '#000000'
        self.maxsize(1366, 766)

    state = WM.state   # type: ignore

    def overrideredirect(self, boolean: Optional[bool] = None):   # type: ignore
        """Not implemented, Use W.SetWindowLongPtrW or Tkinter pure."""
        return super().overrideredirect(boolean)   # type: ignore

    def maxsize(self, width: Optional[int] = None, height: Optional[int] = None) -> tuple[int, int]:   # type: ignore
        super().maxsize(width, height)   # type: ignore
        if width is not None and height is not None:
            self.data['WM_GETMINMAXINFO'][1] = width + 15, height + 8
            W.user32.PostMessageW(Call.hWnd, W.c.WM_GETMINMAXINFO, 0, 0)
        return self.data['WM_GETMINMAXINFO'][1][0] - 15, self.data['WM_GETMINMAXINFO'][1][1] - 8

    def minsize(self, width: Optional[int] = None, height: Optional[int] = None) -> tuple[int, int]:   # type: ignore
        super().minsize(width - 16, height - 39)   # type: ignore
        if width is not None and height is not None:
            self.data['WM_GETMINMAXINFO'][0] = width + 16, height + 39
            W.user32.PostMessageW(Call.hWnd, W.c.WM_GETMINMAXINFO, 0, 0)
        return self.data['WM_GETMINMAXINFO'][0][0] - 16, self.data['WM_GETMINMAXINFO'][0][1] - 39

    def after(self, ms: int, func: Callable[..., None] = None, *_):   # type: ignore
        print(self, '"after" with WM_MOVE produces an error.') if self.settings['Debug']['Info'] else ...
        return super().after(ms, func, *_)

    def title(self, string: str = ''):   # type: ignore
        self.data['WM']['title'] = string if string else self.data['WM'].get('title', '')
        self.S['StringVar'][0].set(self.data['WM']['title']) if self.S['StringVar'] else ...
        return string

    def geometry(self, new_geometry: str = ''):   # type: ignore
        def merge(n: Any): return tuple(map(lambda n: n[0] if n[0] else n[1], n))
        n = merge(zip(*re.findall(r'^(\d+)x(\d+)|([-+]\d+)([-+]\d+)|.*$', new_geometry if new_geometry else '...')[:2]))
        width, height, x, y = map(int, merge(zip(n, (*self.data['WM_SIZE'], *self.data['WM_MOVE']))))
        W.user32.SetWindowPos(Call.hWnd, 0, x, y, width + 16, height + 41, c.SWP_FRAMECHANGED) if any(n) else ...
        WM_SIZE, WM_MOVE = self.data['WM_SIZE'], self.data['WM_MOVE']
        _add, _h = (8, 3) if self.WM.state() == 'zoomed' else (0, 0)
        return '{}x{}{:+}{:+}'.format(WM_SIZE[0] - 2, WM_SIZE[1] - 34 - _h, WM_MOVE[0] - 8 + _add, WM_MOVE[1] + _add)
    """In pure Tkinter, and window state is 'zoom', window position is to 'normal' state. That doesn't happen here."""

    def winfo_x(self) -> int: return self.data['WM_MOVE'][0] - 8

    def winfo_y(self): return self.data['WM_MOVE'][1]

    def winfo_width(self): return self.data['WM_SIZE'][0] - 2

    def winfo_height(self): return self.data['WM_SIZE'][1] - (35 if self.WM.state() == 'zoomed' else 34)

    def winfo_rootx(self) -> int: return self.data['WM_MOVE'][0]

    def winfo_rooty(self) -> int: return self.data['WM_MOVE'][1] + (40 if self.WM.state() == 'zoomed' else 33)

    def mainloop(self, n: int = 0):
        if self.settings['WM']['visible']:
            W.user32.SetLayeredWindowAttributes(Call.hWnd, 255, 255, c.LWA_ALPHA)
        return super().mainloop(n)
