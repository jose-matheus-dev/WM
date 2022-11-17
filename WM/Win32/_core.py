import ctypes as ct
from ctypes import wintypes as wt
from typing import Any

import _ctypes  # type: ignore

LRESULT: Any = type('LRESULT', (_ctypes._SimpleCData, ), {'_type_': 'q'})  # type: ignore
WNDPROC = ct.WINFUNCTYPE(LRESULT, wt.HWND, wt.UINT, wt.WPARAM, wt.LPARAM)  # type: ignore
