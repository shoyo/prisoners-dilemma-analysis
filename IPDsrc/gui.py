from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from main import run_simulation


class SimulationGUI(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(fill=BOTH)
        self.config(bg=bg['default'])

        self.header = Frame(self)
        self.setting_frame = Frame(self)
        self.graph_frame = Frame(self)
        self.footer = Frame(self)

        self.header.grid(row=0, column=0, columnspan=2)
        self.setting_frame.grid(row=1, column=0)
        self.graph_frame.grid(row=1, column=1)
        self.footer.grid(row=2, column=0, columnspan=2)

        self.curr_row = 0

        self.init_strats()
        self.init_params()
        self.init_graph()
        self.init_menu()
        self.init_decor()

    def init_strats(self):
        self.coop_strats = {
            'Kantian': IntVar(),
            'Tit for Tat': IntVar(),
            'Tit for 2 Tats': IntVar(),
            'Grudger': IntVar(),
        }
        self.self_strats = {
            'Defector': IntVar(),
            'Mean Tit for Tat': IntVar(),
            'Conniver': IntVar(),
            'Tester': IntVar()
        }
        self.neut_strats = {
            'Wary Tit for Tat': IntVar(),
            'Random': IntVar(),
        }
        self.all_strats = {
            'Cooperative strategies': self.coop_strats,
            'Selfish strategies': self.self_strats,
            'Neutral strategies': self.neut_strats
        }

        Label(self.setting_frame, text="Initial Profile",
              font=fonts['header'], height=2).grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for strategy_type in self.all_strats:
            Label(self.setting_frame, text=strategy_type, font=fonts['sub_header'],
                  padx=15, width=15).grid(row=self.curr_row)
            self.curr_row += 1
            for strategy in self.all_strats[strategy_type]:
                Label(self.setting_frame, text=strategy + ' -', font=fonts['text'],
                      width=15, anchor=E).\
                    grid(row=self.curr_row, column=0)
                Entry(self.setting_frame, width=entry_width, justify='right',
                      textvariable=self.all_strats[strategy_type][strategy]).\
                    grid(row=self.curr_row, column=1)
                self.curr_row += 1

    def init_params(self):
        self.param = {
            'Rounds': IntVar(),
            'Generations': IntVar()
        }
        self.param['Rounds'].set(10)
        self.param['Generations'].set(35)

        Label(self.setting_frame, text="Simulation settings",
              font=fonts['sub_header'], height=2, width=15, anchor=S).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for param in self.param:
            Label(self.setting_frame, text=param + " -", width=12,
                  anchor=E).grid(row=self.curr_row, column=0)
            Entry(self.setting_frame, width=entry_width, justify='right',
                  textvariable=self.param[param]).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1

        self.clear_button = Button(self.setting_frame, text='Clear',
                                   font=fonts['sub_button'], height=2,
                                   command=self.reset)
        self.clear_button.grid(row=0, column=1)
        self.execute_button = Button(self.setting_frame, text='Execute',
                                     font=fonts['main_button'], height=2,
                                     command=self.confirm, bg='blue')
        self.execute_button.grid(row=self.curr_row, column=1)
        self.curr_row += 1

    def init_presets(self):
        diverse = {
            # just make a function that changes all values to n.
        }
        defectors_among_kantians = {
            'Defector': 3,
            'Kantian': 97
        }
        tft_among_defectors = {
            'Tit for Tat': 3,
            'Defector': 97
        }
        all_presets = {
            'Defectors among Kantians': [defectors_among_kantians, None],
            'TFT among Defectors': [tft_among_defectors, None]
        }
        Label(self.setting_frame, text="~ Presets ~",
              font=fonts['sub_header'], pady=10, width=20).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for preset in all_presets:
            all_presets[preset][1] = Button(self.setting_frame, text='select',
                                            font=fonts['sub_button'],
                                            command=self.select_preset(preset))
            all_presets[preset][1].grid(row=self.curr_row, column=0)
            Label(self.setting_frame, text=preset).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1

    def init_graph(self):
        self.fig = Figure(figsize=(8, 5.7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0)
        self.plot_filler()
        self.graph_label = Label(self.graph_frame, text="tweak settings to display graph!")
        # self.graph_label.grid(row=0, column=0)
        # self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.graph_frame)
        # self.toolbar.update()
        # self.canvas._tkcanvas.grid(row=0, column=0)

    def init_menu(self):
        main_menu = Menu(self.parent)
        file_menu = Menu(main_menu, tearoff=0)
        file_menu.add_command(label='Execute', accelerator='Cmd+E', command=self.execute_plot)
        main_menu.add_cascade(label='File', menu=file_menu)
        self.parent.config(menu=main_menu)

    def init_decor(self):
        self.header.config(bg=bg['decor1'])
        self.footer.config(bg=bg['decor1'])

        Label(self.footer, text="footer", font=fonts['header']).grid(row=0, column=0)

        top_canvas = Canvas(self.header, bg=bg['decor1'], height=25, width=1100)
        top_canvas.grid(row=0, column=0)
        bot_canvas = Canvas(self.footer, bg=bg['decor1'], height=25, width=1100)
        bot_canvas.grid(row=0, column=0)

    def plot_filler(self):
        self.fig.clear()
        self.fig.add_subplot(111).plot()
        self.canvas.show()

    def reset(self):
        self.plot_filler()
        for strat_list in self.all_strats:
            for strat in self.all_strats[strat_list]:
                self.all_strats[strat_list][strat].set(0)

    def compile_profile(self):
        profile = {}
        for strategy_type in self.all_strats:
            for strategy in self.all_strats[strategy_type]:
                try:
                    var = self.all_strats[strategy_type][strategy].get()
                except TclError:
                    messagebox.showerror("Warning",
                                         "Inputted values are invalid. Please try again.")
                    return
                if var != 0:
                    profile[strategy] = var
        return profile

    def confirm(self):
        response = messagebox.askquestion("Confirmation",
                                          "Are you sure you would like to "
                                          "execute this simulation?")
        if response == 'yes':

            self.execute_plot()

    def execute_plot(self):
        result = run_simulation(self.compile_profile(),
                                self.param['Generations'].get(),
                                self.param['Rounds'].get())
        self.fig.clear()
        x_axis = result.pop('gens')
        a = self.fig.add_subplot(111)
        for strat in result:
            a.plot(x_axis, result[strat], label=strat)
        self.canvas.show()

    def quit_app(self):
        self.parent.quit()

    def select_preset(self, preset):
        pass


def run_gui():
    root = Tk()
    root.title("IPD Simulation")
    root.geometry("1090x631")
    root.resizable(False, False)
    ipd = SimulationGUI(root)
    root.mainloop()


fonts = {
    'header': 'Calibri 19 bold',
    'sub_header': 'Calibri 16 bold italic',
    'text': 'Calibri 14',
    'main_button': 'Calibri 14 italic',
    'sub_button': 'Calibri 12'
}

bg = {
    'default': '#DCDCDC',
    'main_button': '#435440',
    'decor1': '#1569C7',
    'test3': '#ffff66',
    'test4': '#7a1018',
    'test5': '#e8db1e'
}

entry_width = 4


if __name__ == '__main__':
    run_gui()
