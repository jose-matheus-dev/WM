"""Win32API for Python with ctypes"""

from ctypes import WinDLL  # type: ignore

from . import constants, structures
from ._core import LRESULT as LRESULT  # noqa: F401
from ._core import WNDPROC as WNDPROC  # noqa: F401
from ._core import Any, ct, wt

gdi32: Any = WinDLL('gdi32', use_last_error=True)
user32: Any = WinDLL('user32', use_last_error=True)
dwmapi: Any = WinDLL('dwmapi', use_last_error=True)
uxtheme: Any = WinDLL('uxtheme', use_last_error=True)
kernel32: Any = WinDLL('kernel32', use_last_error=True)

s, c = structures, constants

hInst = kernel32.GetModuleHandleW(None)


class hWnd(int):
    ...


user32.DefWindowProcW.argtypes = [wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM]


# define LOWORD(l)         ((WORD)(((DWORD_PTR)(l)) & 0xffff))
def LOWORD(dwValue: wt.LPARAM): return int(dwValue) & 0xffff


# define HIWORD(l)         ((WORD)((((DWORD_PTR)(l)) >> 16) & 0xffff))
def HIWORD(dwValue: wt.LPARAM): return (int(dwValue) >> 16) & 0xffff


# define GET_X_LPARAM(lp)             ((int)(short)LOWORD(lp))
def GET_X_LPARAM(lp: wt.LPARAM): return ct.c_short(LOWORD(lp)).value


# define GET_Y_LPARAM(lp)             ((int)(short)HIWORD(lp))
def GET_Y_LPARAM(lp: wt.LPARAM): return ct.c_short(HIWORD(lp)).value
