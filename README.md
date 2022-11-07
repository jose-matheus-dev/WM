# WM
A Window Manager for Tkinter On Windows 10

[To Move](https://user-images.githubusercontent.com/73524758/175761318-5dea6c64-f1c1-410e-8abf-7adaa1b886a8.mp4)

## How to use
>~~~Python
>from WM import TK
>
>...
>
>if __name__ == '__main__':
>    Tk = TK()
>    TK.mainloop()
>~~~

I developed a code pattern based on the Sword Art Online (SAO) for Tkinter

###  For Example:

**`System Call Generate`** `Button` **`Element`** `<Object-ID>` _`Discharge`_ !

_Discharge_ is only a SAO reference.

[`./TK/ref/__init__.py`](./TK/ref/__init__.py)
> ~~~Python
> class Call:  # Object-IDs are here.
>    Tk, ... = tk.Tk, ...
>    W = {'B': list[Button], ...}  # W['B'][-1] for the last Button
>
> class System(Call):  # class TK(System, Call.Tk): 
>    Call = Call  # System.Call
> ~~~

 [`./TK/ref/views.py`](./TK/ref/views.py)
> ~~~python
> class Element(System, Call):
>    def __init__(self, N: str = '', *_, generic=0, **__: ...):
>        super(System, self).__init__()  # info when called
>    # Accelerators for Grid, Pack and Cropping to Image
>
> class Generate(System, Call):
>    def __init__(self):
>        super(System, self).__init__()  # info when called
>        ...
>        # with Element Constructor
>        Element('Frame', self.TK).grid(0, 0, 'nsew', padx=1, pady=1)({0: (1, 1), 1: (0, 1), 2: (1, 0)}).grid_remove()
>        self.W['F'][-1].grid()
>        # another way to do the same
>        my_frame = ttk.Frame(self.TK)
>        my_frame.grid(row=0, column=0, sticky='nsew', padx=1, pady=1)
>        my_frame.grid_rowconfigure(0, weight=1)
>        my_frame.grid_rowconfigure(2, weight=1)
>        my_frame.grid_columnconfigure(0, weight=1)
>        my_frame.grid_columnconfigure(1, weight=1)
>        my_frame.grid_remove()
>        my_frame.grid()
> ~~~




