import tkinter as tk, tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
import random as rand
import time


class RenderApp:
    def __init__(self):
        self.app_state = None
        self.app_state = None
        self.current_index = 0
        self.values = []
        self.bars = []

        self.build_window()

    @staticmethod
    def normalize_input(list):
        for i in range(len(list)):
            list[i] = float(list[i])
        biggest = max(list)
        scalar = 600 / biggest
        outlist = []

        for item in list:
            outlist.append(item * scalar)
        return outlist

    def update(self, frame):
        stime = time.time()
        bar_width = 1000 / len(self.values)
        for x in range(len(self.values)):
            bar = tk.Frame(
                master=frame,
                width=bar_width,
                height=self.values[x],
                bg="red" if x == self.current_index else "black",
                highlightbackground="light grey",
                highlightthickness=1,
            )
            bar.grid(row=0, column=x, sticky="s")
            self.bars.append(bar)
        etime = stime - time.time()
        return etime

    def build_window(self):
        self.app_state = "Preparing"
        self.window = tk.Tk()
        window = self.window
        window.resizable(width=False, height=False)
        window.title("Sorter Renderer")

        self.mainframe = tk.Frame(master=window, width=1000, height=600)
        mainframe = self.mainframe
        mainframe.pack()

        self.anim_frame = tk.Frame(master=mainframe, width=1000, height=600)
        anim_frame = self.anim_frame
        anim_frame.rowconfigure(0, weight=1)
        anim_frame.grid_propagate(False)
        anim_frame.grid(row=0, column=0, sticky="nsew")

        self.divider_frame = tk.Frame(master=mainframe, background="black")
        self.divider_frame.grid(row=1, column=0, sticky="nsew")

        etime = 0
        info_frame = tk.Frame(master=mainframe)
        self.render_button = tk.Button(
            master=info_frame,
            relief=tk.RAISED,
            text="Load File",
            command=self.handle_render_button,
        )
        render_button = self.render_button
        self.info_label = tk.Label(master=info_frame, text="")
        time_label = tk.Label(master=info_frame, text=f"time elapsed: {etime} seconds")

        info_frame.grid(row=2, column=0, sticky="nsew")
        render_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.info_label.pack(side=tk.RIGHT)
        time_label.pack(side=tk.LEFT)

        # etime = self.update(anim_frame)

        self.app_state = "Waiting for input"

        window.mainloop()

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepath:
            self.info_label.config(text="Invalid file path. Please try again.")
            return
        try:
            with open(filepath, mode="r", encoding="utf-8") as input_file:
                input_list = input_file.readlines()
        except:
            self.info_label.config(
                text="Invalid file type or contents. Please try again."
            )

        self.values = RenderApp.normalize_input(input_list)

    def handle_render_button(self):
        if self.app_state == "Waiting for input":
            self.open_file()
            self.update(self.anim_frame)
            self.render_button.config(text="Render")
            self.app_state = "Ready"

        elif self.app_state == "Ready":
            self.app_state = "Running"
            for bar in self.bars:
                bar.destroy()
            self.bars = []

            # do one step of sorting
            self.update(self.anim_frame)

        elif self.app_state == "Running":
            self.app_state = "Ready"
            self.update(self.anim_frame)


def main():
    app = RenderApp()


if __name__ == "__main__":
    main()
