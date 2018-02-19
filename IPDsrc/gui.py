from tkinter import *
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
        self.pack(fill=BOTH)
        self.config(bg=bg['test'])

        self.setting_frame = Frame(self)
        self.preset_frame = Frame(self)
        self.graph_frame = Frame(self)

        self.setting_frame.grid(row=0, column=0)
        self.preset_frame.grid(row=1, column=0)
        self.graph_frame.grid(row=0, column=1)

        self.curr_row = 0

        self.init_strats()
        self.init_params()
        self.init_presets()
        self.init_graph()

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
                  padx=15, width=20, anchor=W).grid(row=self.curr_row)
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
              font=fonts['sub_header'], height=2, width=20, anchor=SW).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for param in self.param:
            Label(self.setting_frame, text=param + " -", width=12,
                  anchor=E).grid(row=self.curr_row, column=0)
            Entry(self.setting_frame, width=entry_width, justify='right',
                  textvariable=self.param[param]).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1

        self.reset_button = Button(self.setting_frame, text='Reset',
                                   font=fonts['sub_button'], height=2,
                                   command=self.reset_strat_values)
        self.reset_button.grid(row=0, column=1)
        self.execute_button = Button(self.setting_frame, text='Execute',
                                     font=fonts['main_button'], height=2,
                                     command=self.confirmation)
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

        Label(self.preset_frame, text="~ Presets ~",
              font=fonts['sub_header'], pady=10, width=20).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for preset in all_presets:
            all_presets[preset][1] = Button(self.preset_frame, text='select',
                                            font=fonts['sub_button'],
                                            command=self.select_preset(preset))
            all_presets[preset][1].grid(row=self.curr_row, column=0)
            Label(self.preset_frame, text=preset).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1

    def init_graph(self):
        self.sample_fig = Figure(figsize=(5, 5), dpi=100)
        a = self.sample_fig.add_subplot(111)
        a.plot()
        canvas = FigureCanvasTkAgg(self.sample_fig, self)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=1)

    def reset_strat_values(self):
        for strat_list in self.all_strats.keys():
            for strat in self.all_strats[strat_list].keys():
                self.all_strats[strat_list][strat].set(0)

    def compile_profile(self):
        profile = {}
        for strategy_type in self.all_strats:
            for strategy in self.all_strats[strategy_type]:
                try:
                    var = self.all_strats[strategy_type][strategy].get()
                except TclError:
                    if var == "":
                        self.all_strats[strategy_type][strategy].set(0)
                    messagebox.showerror("Warning", "Inputted values were invalid. Graph may be wrong")
                if var == 0:
                    continue
                profile[strategy] = var
        return profileerror

    def confirmation(self):
        response = messagebox.askquestion("Confirmation",
                                          "Are you sure you would like to "
                                          "execute this simulation?")
        if response == 'yes':
            self.execute_plot()

    def execute_plot(self):
        canvas = FigureCanvasTkAgg(self.sample_fig, self)
        result = run_simulation(
            self.compile_profile(), self.param['Generations'].get(), self.param['Rounds'].get())
        x_axis = result.pop('gens')
        a = self.sample_fig.add_subplot(111)
        for strat in result:
            a.plot(x_axis, result[strat], label=strat)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=1)

    def select_preset(self, preset):
        pass


def run_gui():
    root = Tk()
    root.title("IPD Simulation")
    root.minsize(950, 700)
    root.geometry("950x700")

    ipd = SimulationGUI(root)
    root.mainloop()


fonts = {
    'header': 'Calibri 19 bold',
    'sub_header': 'Calibri 16 bold italic',
    'text': 'Calibri 14',
    'main_button': 'Calibri 16 italic',
    'sub_button': 'Calibri 12'
}

bg = {
    'test': '#BEF9FB',
    'test1': '#435440',
    'test2': '#c15549',
    'test3': '#ffff66',
    'test4': '#7a1018',
    'test5': '#e8db1e'
}

entry_width = 4


if __name__ == '__main__':
    run_gui()
