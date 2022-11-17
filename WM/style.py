from .core import Call, Path, System
from .TK import E


class Style(System, E.Style):
    def __init__(self, ):
        super().__init__()

        settings = {
            'TFrame': {
                'configure': {
                    'background': self.COLORS['bar'][0]
                },
            },
            'TLabel': {
                'configure': {
                    'background': self.COLORS['bar'][0],
                    'font': ('Yu Gothic UI', 14),
                    'foreground': '#ffffff',
                },
                'layout': [
                    ('Label.padding', {'children': [(
                        'Label.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})
                ],
            },
            'TButton': {
                'configure': {
                    'background': self.COLORS['bar'][0],
                    'padding': (17, 10, 17, 11),
                },
                'layout': [('Button.padding', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})],
            },
            'bar.TFrame': {
                'configure': {
                    'background': self.COLORS['bar'][0]
                },
                'layout': [('Frame.padding', {'sticky': 'nswe'})],
            },
            'bar.TLabel': {
                'configure': {
                    'background': self.COLORS['bar'][0],
                    'font': ('Yu Gothic UI', 10),
                    'foreground': '#ffffff',
                    'anchor': 'w',
                    'padding': (10, 0, 10, 5),
                },
                'map': {
                    'foreground': [('!background', '#858585')]
                },
                'layout': [
                    ('Label.padding', {'children': [(
                        'Label.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})
                ],
            },
            'bar.TButton': {
                'configure': {
                    'background': self.COLORS['bar'][0],
                    'padding': (17, 10, 17, 11),
                    'anchor': 'nw'
                },
                'layout': [('Button.padding', {'children': [('Button.label', {'sticky': 'nswe'})], 'sticky': 'nswe'})],
            }
        }
        self.theme_create('WM', parent='default', settings=settings)  # type: ignore
        self.theme_use('WM')
        self.set_styles()
        self.set_images()

    def set_styles(self):
        if Call.data['WM'].get('title', False):
            self.W['L'][0]['style'] = 'title.bar.TLabel'
        self.W['F'][0]['style'] = 'bar.TFrame'
        """ for i, s in enumerate(('min', 'max', 'exit')):
            self.W['B'][i]['style'] = f'{s}.TButton'
        # minimize maximize exit """
        self.W['Button'][0]['style'] = 'minimize.bar.TButton'
        self.W['Button'][1]['style'] = 'maximize.bar.TButton'
        self.W['Button'][2]['style'] = 'exit.bar.TButton'

    def set_images(self):
        image = E.PhotoImage(file=Path('WM', __file__)('images\\0-00-000.png'))
        for i in range(3):
            E.PhotoImage().cropping(i * 12, 0, (i + 1) * 12, 12, image)
            self.configure(self.W['B'][i]['style'], image=self.S['PhotoImage'][-1])
            E.PhotoImage().cropping(i * 12, 12, (i + 1) * 12, 24, image)
            self.map(self.W['B'][i]['style'], background=[
                ('active', self.COLORS['bar'][1] if i != 2 else self.COLORS['bar'][2])])
            if i != 1:
                self.map(self.W['B'][i]['style'], image=[
                    ('!alternate', 'active', self.S['PhotoImage'][-2]),
                    ('!alternate', '!background', self.S['PhotoImage'][-1])])
            else:
                self.map(self.W['B'][i]['style'], image=[
                    ('!alternate', 'active', self.S['PhotoImage'][-2]),
                    ('!alternate', '!background', self.S['PhotoImage'][-1]),
                    ('alternate', 'background', E.PhotoImage().cropping(36, 0, 48, 12, image)),
                    ('alternate', 'active', self.S['PhotoImage'][-1]),
                    ('alternate', '!background', E.PhotoImage().cropping(36, 12, 48, 24, image))])
