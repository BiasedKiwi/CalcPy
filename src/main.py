import operator

from typing import *
from tkinter import *
from tkinter import ttk
import tkinter as tk
from enum import Enum

from constants import *


class Operations(Enum):
    SUM = operator.add
    DIFF = operator.sub
    PRODUCT = operator.mul
    QUOTIENT = operator.truediv
    END = None  # Last number
    RESULT = None


def main():
    root = tk.Tk()
    root.geometry("500x200")
    root.title("Calculator")

    n_current = tk.StringVar(root, "0")
    buffer = []

    def add_number(n: str, n_field: ttk.Label):
        if str(n_field.cget("text")) == "0":
            n_current.set(n)
        else:
            n_current.set(n_current.get() + n)

    def save_buffer(n_field: tk.Label, op: Operations):
        nonlocal buffer

        try:
            id = buffer[-1]["id"] + 1
        except IndexError:
            id = 0

        try:  # There's probably a better way to do this
            if buffer[-1]["operation"] == Operations.RESULT:
                cached = buffer[-1]
                cached["operation"] = op
                cached["id"] = 0
                buffer = [cached]
            else:
                buffer.append({"value": n_field.cget("text"), "operation": op, "id": id})
        except IndexError:
            buffer.append({"value": n_field.cget("text"), "operation": op, "id": id})
        n_current.set("0")
        print(buffer)

    def calc(n_field: tk.Label):
        save_buffer(n_field, Operations.END)
        result = 0
        last = None
        for number in buffer:
            if last is not None:
                result = last["operation"].value(
                    float(last["value"]), float(number["value"])
                )
                if number["operation"] == Operations.END:
                    continue
            else:
                last = number
                continue

        n_current.set(result)
        buffer.append({"value": str(result), "operation": Operations.RESULT, "id": len(buffer) + 1})  # Convert `result` to string for good measure
        return result

    def all_clear():
        nonlocal buffer

        buffer = []
        n_current.set("0")

    def clear():
        n_current.set("0")

    function_l = [add_number, save_buffer, calc, all_clear, clear]

    number_field = render_number_field(root, n_current)
    render_buttons(root, number_field, function_l)

    root.mainloop()


# pylint: disable=line-too-long
def render_number_field(
    window: tk.Tk, buffer: List[Dict[str, str | Operations | int]]
) -> ttk.Label:
    number_frame = tk.Frame(window)
    number_frame.pack()

    number_field = ttk.Label(number_frame, textvariable=buffer)
    number_field.pack()

    return number_field


# pylint: disable=unnecessary-lambda
def render_buttons(window: tk.Tk, number_field: ttk.Label, functions: List[Callable]):
    current_row = 0
    current_column = 0

    btn_frame = tk.Frame(window)
    btn_frame.pack()

    buttons = [
        ttk.Button(
            btn_frame, text="7", command=lambda: functions[0]("7", number_field)
        ),
        ttk.Button(
            btn_frame, text="4", command=lambda: functions[0]("4", number_field)
        ),
        ttk.Button(
            btn_frame, text="1", command=lambda: functions[0]("1", number_field)
        ),
        ttk.Button(
            btn_frame, text="8", command=lambda: functions[0]("8", number_field)
        ),
        ttk.Button(
            btn_frame, text="5", command=lambda: functions[0]("5", number_field)
        ),
        ttk.Button(
            btn_frame, text="2", command=lambda: functions[0]("2", number_field)
        ),
        ttk.Button(
            btn_frame, text="9", command=lambda: functions[0]("9", number_field)
        ),
        ttk.Button(
            btn_frame, text="6", command=lambda: functions[0]("6", number_field)
        ),
        ttk.Button(
            btn_frame, text="3", command=lambda: functions[0]("3", number_field)
        ),
        ttk.Button(
            btn_frame, text="0", command=lambda: functions[0]("0", number_field)
        ),
        ttk.Button(
            btn_frame, text=".", command=lambda: functions[0](".", number_field)
        ),
        ttk.Button(
            btn_frame,
            text="AC",
            command=lambda: functions[3](),
        ),
        ttk.Button(
            btn_frame,
            text="C",
            command=lambda: functions[4](),
        ),
        ttk.Button(
            btn_frame,
            text="+",
            command=lambda: functions[1](number_field, Operations.SUM),
        ),
        ttk.Button(
            btn_frame,
            text="-",
            command=lambda: functions[1](number_field, Operations.DIFF),
        ),
        ttk.Button(
            btn_frame,
            text="*",
            command=lambda: functions[1](number_field, Operations.PRODUCT),
        ),
        ttk.Button(
            btn_frame,
            text="/",
            command=lambda: functions[1](number_field, Operations.QUOTIENT),
        ),
        ttk.Button(btn_frame, text="=", command=lambda: functions[2](number_field)),
    ]
    for btn in buttons:
        if current_row > MAX_COLUMN:
            current_column += 1
            current_row = 0
        current_row += 1
        btn.grid(row=current_row, column=current_column)


if __name__ == "__main__":
    main()
