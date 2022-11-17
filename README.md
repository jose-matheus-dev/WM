# WM
A Window Manager for Tkinter On Windows 10

[Video Test](https://user-images.githubusercontent.com/73524758/200260996-18de1043-4b5f-4f9c-b3ee-6e27d1903594.mp4)
* [WM/Wiki](https://github.com/XxFULLDLCxX/WM/wiki)

## How to install
```Bash
pip install 574d
```

## How to test
> ```Python
> from WM import TK
>
> ...
>
> if __name__ == '__main__':
>     Tk = TK()
>     Tk.mainloop()
> ```

I developed a code pattern based on the Sword Art Online (SAO) for Tkinter

###  For Example:

**`System Call Generate`** `Button` **`Element`** `<Object-ID>` _`Discharge`_ !

_Discharge_ is only a SAO reference.

[`./WM/core.py`](./WM/core.py)
> ```Python
> class Call(TkData, INHERIT):  # Object-IDs are here.
>     ...
>     szTitle, szWindowClass = 'WM', 'WM'
>     ...
>
> class System(Call):  # class TK(System, Call.Tk): 
>     Call = Call  # System.Call
>     ...
> ```

 [`./WM/views.py`](./WM/views.py)
> ```python
> class Element(E.Widget, E.PhotoImage, System, Call):  # type: ignore
>     def __new__(cls, name: str = '', *_: E.Any, generic: bool = False, **__: E.Any):
>         E = GENERATE.__dict__[name](*_, **__)
>         if generic:
>             del E._[-1]
>         return E
>
>
> class Generate(System, Call):
>     def __init__(self):
>         super(System, self).__init__()  # info when called
>         ...
>         # with Element Constructor
>         Element('Frame', self.TK).grid(0, 0, 'nsew', padx=1, pady=1)({0: (1, 1), 1: (0, 1), 2: (1, 0)}).grid_remove()
>         self.W['F'][-1].grid()
>         # another way to do the same
>         my_frame = ttk.Frame(self.TK)
>         my_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
>         my_frame.grid_rowconfigure(0, weight=1)
>         my_frame.grid_rowconfigure(2, weight=1)
>         my_frame.grid_columnconfigure(0, weight=1)
>         my_frame.grid_columnconfigure(1, weight=1)
>         my_frame.grid_remove()
>         my_frame.grid()
> ```




