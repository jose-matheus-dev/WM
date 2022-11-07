from WM import TK
from WM.core import System, Call


class Event(System):
    def __init__(self):
        self.TK.bind('<<WM_SIZE>>', self.WM_SIZE)

    def WM_SIZE(self, event: ...):
        self.S['StringVar'][0].set(f'{event.x_root}x{event.y_root}')


class APP(TK):
    def __init__(self):
        super().__init__()
        self.title('In Title Bar Label')
        self.geometry('320x468')
        self.config(bg='#0000EE')


if __name__ == '__main__':
    System.szTitle = 'Window Name'
    System.szWindowClass = 'Window Class'
    System.settings['Debug']['Info'] = True
    APP()(Event)
    Call.TK.mainloop()