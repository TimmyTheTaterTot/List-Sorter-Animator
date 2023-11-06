import tkinter as tk, tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
import time


class RenderApp:
    def __init__(self):
        # setup variables and build the Application Window
        self.app_state = None
        self.current_index = 0
        self.top_index = None
        self.values = []
        self.values_len = None
        self.bars = []

        self.etime = 0
        self.stime = 0

        self.build_window()

    @staticmethod
    def normalize_input(list):
        # takes in a list as input and scales the values so they fit vertically
        for i in range(len(list)):
            list[i] = float(list[i])
        biggest = max(list)
        scalar = 600 / biggest
        outlist = []

        for item in list:
            outlist.append(item * scalar)
        return outlist

    def sort_one(self):
        # performs one sorting calculation and updates the display
        # cache object values for easier reference
        lst = self.values
        i = self.current_index

        # if the algorithm has reached the top, check if the list is sorted, then reset to the bottom if not
        if i == self.top_index:
            if not lst == sorted(lst):
                self.top_index -= 1
                self.current_index = 1
                i = 1
            else:
                self.app_state = "Finished"
                self.info_label.config(text="")
                return

        # do one bar swap
        if lst[i] < lst[i - 1]:
            lst.insert(i - 1, lst.pop(i))
            self.update(self.anim_frame, i)
            self.current_index += 1
        else:
            self.current_index += 1
            self.sort_one()
            return

        # refresh screen
        self.window.after(50, self.sort_one)

    def update(self, frame, curr_index):
        # updates the display by 1) removing all bars 2) regenerating all bars based on sorted list
        for bar in self.bars:
            bar.destroy()
        self.bars = []

        bar_width = 1000 / len(self.values)
        for x in range(len(self.values)):
            bar = tk.Frame(
                master=frame,
                width=bar_width,
                height=self.values[x],
                bg="red" if x == curr_index else "black",
                highlightbackground="light grey",
                highlightthickness=1,
            )
            bar.grid(row=0, column=x, sticky="s")
            self.bars.append(bar)

        # update elapsed time display
        self.etime = time.time() - self.stime
        self.time_label.config(text=f"time elapsed: {round(self.etime, 3)} seconds")

    def build_window(self):
        # sets up main window with all the assets needed to run the program
        self.app_state = "Preparing"
        self.window = tk.Tk()
        window = self.window
        window.resizable(width=False, height=False)
        window.title("Sorter Renderer")

        # mainframe holds all the child frames
        self.mainframe = tk.Frame(master=window, width=1000, height=600)
        mainframe = self.mainframe
        mainframe.pack()

        # anim frame holds all the bars that are being animated
        self.anim_frame = tk.Frame(master=mainframe, width=1000, height=600)
        anim_frame = self.anim_frame
        anim_frame.rowconfigure(0, weight=1)
        anim_frame.grid_propagate(False)
        anim_frame.grid(row=0, column=0, sticky="nsew")

        # divider frame makes a small divider line at the bottom of the screen
        self.divider_frame = tk.Frame(master=mainframe, background="black")
        self.divider_frame.grid(row=1, column=0, sticky="nsew")

        # info frame stores info about the running simulation and the interaction button
        info_frame = tk.Frame(master=mainframe)
        self.render_button = tk.Button(
            master=info_frame,
            relief=tk.RAISED,
            text="Load File",
            command=self.handle_render_button,
        )
        render_button = self.render_button
        self.info_label = tk.Label(master=info_frame, text="")
        self.time_label = tk.Label(
            master=info_frame, text=f"time elapsed: {self.etime} seconds"
        )

        info_frame.grid(row=2, column=0, sticky="nsew")
        render_button.pack(side=tk.RIGHT, padx=5, pady=5)
        self.info_label.pack(side=tk.RIGHT)
        self.time_label.pack(side=tk.LEFT)

        # update app state and begin animation loop
        self.app_state = "Waiting for input"

        window.mainloop()

    def open_file(self):
        # uses the file dialogue to get input for and process a file into a list of numbers
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

        # takes the string list and passes it to normalize input to get back a normalized list of floats instead
        self.values = RenderApp.normalize_input(input_list)
        self.values_len = len(self.values)

    def handle_render_button(self):
        # handles user input on the render button, changing behavior based on app state
        # if there is no input yet, the button should prompt the user to input a source file
        if self.app_state == "Waiting for input":
            self.open_file()
            self.update(self.anim_frame, None)
            self.render_button.config(text="Render")
            self.app_state = "Ready"

        # if a source file is already input, it should run the simuation
        elif self.app_state == "Ready":
            self.app_state = "Running"
            self.info_label.config(text="Running Simulation...")
            self.top_index = self.values_len
            self.stime = time.time()
            self.sort_one()


def main():
    app = RenderApp()


if __name__ == "__main__":
    main()
