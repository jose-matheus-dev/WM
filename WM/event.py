from .core import Call, System, W, c, ct, s, wt, E


@W.WNDPROC
class WndProc:

    @classmethod
    def __info__(cls, hWnd: wt.HWND, uMsg: wt.UINT, wParam: wt.WPARAM, lParam: wt.LPARAM):
        match uMsg:
            case c.WM_CREATE: print('WM_CREATE')
            case c.WM_DESTROY: print('WM_DESTROY')
            case _: ...

    def __new__(cls, *_: E.Any):
        cls.__info__(*_) if Call.settings['Debug']['Info'] else ...
        return cls.__TK__(*_) if Call.WM else cls.__Win32__(*_)

    @classmethod
    def __Win32__(cls, hWnd: wt.HWND, uMsg: wt.UINT, wParam: wt.WPARAM, lParam: wt.LPARAM):
        match uMsg:
            case c.WM_DESTROY: W.user32.PostQuitMessage(0)
            case _: return W.user32.DefWindowProcW(hWnd, uMsg, wParam, lParam)
        return 0

    @classmethod
    def __TK__(cls, hWnd: wt.HWND, uMsg: wt.UINT, wParam: wt.WPARAM, lParam: wt.LPARAM):
        match uMsg:
            case c.WM_CREATE: Call.hWnd = W.hWnd(hWnd)
            case c.WM_MOVE:
                Call.data |= {'WM_MOVE': (W.GET_X_LPARAM(lParam), W.GET_Y_LPARAM(lParam))}
                Call.TK.event_generate('<<WM_MOVE>>', x=W.GET_X_LPARAM(lParam), y=W.GET_Y_LPARAM(lParam))
            case c.WM_SIZE:
                __add = -5 if int(wParam) == c.SIZE_MAXIMIZED else 1
                Call.TK.event_generate('<<WM_SIZE>>', rootx=W.LOWORD(lParam) + 2, rooty=W.HIWORD(lParam) + __add)
                Call.data |= {'WM_SIZE': (W.LOWORD(lParam) + 2, W.HIWORD(lParam) + __add)}
                Call.WM.geometry(f'{W.LOWORD(lParam) - 16}x{W.HIWORD(lParam)}+0+0')
                Call.WM.update()
            case c.WM_NCCALCSIZE if wParam:
                pncc = s.NCCALCSIZE_PARAMS.from_address(int(lParam))
                pncc.rgrc[0].bottom -= (0 if Call.WM.state() == 'zoomed' else 8)
                pncc.rgrc[0].right -= 8
                pncc.rgrc[0].left += 8
                pncc.rgrc[0].top += 0
                return 0
            case c.WM_GETMINMAXINFO:
                pmmi = s.MINMAXINFO.from_address(int(lParam))
                pmmi.ptMinTrackSize.x, pmmi.ptMinTrackSize.y = Call.data['WM_GETMINMAXINFO'][0]
                pmmi.ptMaxTrackSize.x, pmmi.ptMaxTrackSize.y = Call.data['WM_GETMINMAXINFO'][1]
            case c.WM_ACTIVATE:
                margins = s.MARGINS()
                if wParam:  # Make sure if the Window is Activate.
                    margins.cyTopHeight = 1  # Create a Top border
                    Call.TK.event_generate('<<Activate>>')
                else:
                    Call.TK.event_generate('<<Inactivate>>')
                W.dwmapi.DwmExtendFrameIntoClientArea(hWnd, ct.byref(margins))
            case c.WM_DESTROY:
                Call.TK.destroy()
                W.user32.PostQuitMessage(0)
            case _: return W.user32.DefWindowProcW(hWnd, uMsg, wParam, lParam)

        return System.data['WndProc'](hWnd, uMsg, wParam, lParam) if System.data.get('WndProc', False) else 0


class Event(System):
    def __init__(self):
        super().__init__()

        self.W['B'][0]['command'] = self.wm_minsize
        self.W['B'][1]['command'] = self.wm_maxsize
        self.W['B'][2]['command'] = self.wm_destroy

        self.WM.bind('<Configure>', self.wm_size)
        self.WM.bind('<Motion>', self.wm_hittest)
        self.TK.bind('<Button-1>', self.wm_focus)

        self.W['L'][0].bind('<Button-1>', self.wm_move)
        # WM_GETMINMAXINFO
        self.W['L'][0].bind('<Double-Button-1>', self.wm_maxsize)

        # WM_ACTIVATE
        self.TK.bind('<<Activate>>', self.wm_activate)
        self.TK.bind('<<Inactivate>>', self.wm_inactivate)

    def wm_size(self, *_: E.Any):
        _add = (35, 40) if self.WM.state() == 'zoomed' else (34, 33)
        self.W['F'][0].grid(pady=7 if self.WM.state() == 'zoomed' else 0)
        self.TK.wm_geometry(f"{self.data['WM_SIZE'][0]-18}x{abs(self.data['WM_SIZE'][1]-_add[0])}+0+{_add[1]}")
        nn = '' if self.WM.state() == 'zoomed' else '!'
        self.WM.tk.call(self.W['B'][1], 'state', nn + 'alternate')

    def wm_focus(self, *_: E.Any):
        W.user32.SetFocus(Call.TK.hWnd)
        W.user32.SendMessageW(Call.hWnd, c.WM_ACTIVATE, c.WA_ACTIVE, 0)

    def wm_move(self, event: E.Any):
        W.user32.ReleaseCapture()
        W.user32.PostMessageW(Call.hWnd, c.WM_NCLBUTTONDOWN, self.wm_hittest(event), 0)

    def wm_hittest(self, event: E.Any):
        ptMouse, rcWindow = s.POINT(event.x_root, event.y_root), s.RECT()
        W.user32.GetWindowRect(Call.hWnd, ct.byref(rcWindow))
        uCol, uRow, BORDER = 1, 1, 6
        if ptMouse.x - rcWindow.left < BORDER:
            uCol = 0
        elif ptMouse.x - rcWindow.left > rcWindow.right - rcWindow.left - BORDER:
            uCol = 2
        if ptMouse.y - rcWindow.top < BORDER:
            uRow = 0
        elif ptMouse.y - rcWindow.top > rcWindow.bottom - rcWindow.top - BORDER:
            uRow = 2

        cursors = (('size_nw_se', 'size_ns', 'size_ne_sw'),
                   ('size_we', 'arrow', 'size_we'),
                   ('size_ne_sw', 'size_ns', 'size_nw_se'))
        event.widget['cursor'] = cursors[uRow][uCol]
        hittests = ((c.HTTOPLEFT, c.HTTOP, c.HTTOPRIGHT),
                    (c.HTLEFT, c.HTCAPTION, c.HTRIGHT),
                    (c.HTBOTTOMLEFT, c.HTBOTTOM, c.HTBOTTOMRIGHT))
        return hittests[uRow][uCol]

    def wm_maxsize(self, *_: E.Any):
        self.wm_restore() if self.WM.state() == 'zoomed' else W.user32.ShowWindow(Call.hWnd, c.SW_MAXIMIZE)

    def wm_minsize(self, *_: E.Any): W.user32.ShowWindow(Call.hWnd, c.SW_MINIMIZE)

    def wm_restore(self, *_: E.Any): W.user32.ShowWindow(Call.hWnd, c.SW_RESTORE)

    def wm_destroy(self, *_: E.Any): W.user32.PostMessageW(Call.hWnd, c.WM_CLOSE, 0, 0)

    def wm_activate(self, *_: E.Any):
        """Called when the window is activated."""
        [element.tk.call(element, 'state', 'background') for element in self.W['B'] + self.W['L']]
        #: self.WM.update() This produces a bug when the inactive window is activated by pressing the bottom edge.
        self.WM.update_idletasks()  # It's necessary so that there is no delay in the update when clicking on the edges.

    def wm_inactivate(self, *_: E.Any):
        """Called when the window is inactivated."""
        [element.tk.call(element, 'state', '!background') for element in self.W['B'] + self.W['L']]
