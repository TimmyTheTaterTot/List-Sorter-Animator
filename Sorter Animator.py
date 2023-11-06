import tkinter as tk, tkinter.ttk as ttk
import random as rand
import time


class RenderApp:
    def __init__(self):
        self.app_state = None
        self.col_num = 100
        self.app_state = None

        self.build_window()

    def update(self, mainframe):
        stime = time.time()
        for x in range(self.col_num):
            bar = tk.Frame(
                master=mainframe,
                width=10,
                height=rand.randint(100, 600),
                bg="black",
                highlightbackground="light grey",
                highlightthickness=1,
            )
            bar.grid(row=0, column=x, sticky="s")
        etime = stime - time.time()
        return etime

    def build_window(self):
        self.app_state = "Preparing"
        self.window = tk.Tk()
        self.window.title("Sorter Renderer")

        mainframe = tk.Frame(width=1000, height=600)
        mainframe.pack()

        etime = 0
        info_frame = tk.Frame(width=200)
        render_button = tk.Button(
            master=info_frame,
            relief=tk.RAISED,
            text="Begin Sort",
            command=self.handle_buttonpress,
        )
        time_label = tk.Label(master=info_frame, text=f"time elapsed: {etime} seconds")

        info_frame.pack(fill=tk.X)
        render_button.pack(side=tk.RIGHT, padx=5, pady=5)
        time_label.pack(side=tk.LEFT)

        etime = self.update(mainframe)

        self.app_state = "Ready"

        self.window.mainloop()

    def handle_buttonpress(self):
        if self.app_state == "Ready":
            self.app_state = "Running"


def main():
    app = RenderApp()


if __name__ == "__main__":
    main()
