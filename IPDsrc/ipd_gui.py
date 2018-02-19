import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure

from tkinter import *
from tkinter import messagebox

import main

""" Graphical user interface (GUI) for the Evolutionary Iterated
Prisoner's Dilemma simulation. 
"""

# ----- GUI ----- #

class SimulationGUI(Frame):
    """ Tkinter GUI for evolutionary IPD simulation. """

    # ----- Widget initialization ----- #
    def __init__(self, parent):
        """ Initializes GUI.
        Parent is parent widget, which should be root.
        """
        super().__init__(parent)
        self.parent = parent
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
        self.init_parameters()
        self.init_presets()
        self.init_graph()

    def init_strats(self):
        """ Initializes widgets related to strategies and
        corresponding entry fields.
        """
        # ----- Strategies ----- #
        """ Each strategy indexes its Tkinter textvariable. """

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

        # ----- GUI ----- #

        Label(self.setting_frame, text="Initial Profile", font=fonts['header'],
              height=2).grid(row=self.curr_row, column=0)
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

    def init_parameters(self):
        """ Initializes widgets related to simulation parameters and
        execution buttons.
        """
        # ----- Parameter ----- #
        """ Each parameter indexes its Tkinter variable. """

        self.parameters = {
            'Rounds': IntVar(),
            'Generations': IntVar()
        }

        # ----- GUI ----- #
        Label(self.setting_frame, text="Simulation settings",
              font=fonts['sub_header'], height=2, width=20, anchor=SW).\
            grid(row=self.curr_row, column=0)
        self.curr_row += 1

        for param in self.parameters:
            Label(self.setting_frame, text=param + " -", width=12,
                  anchor=E).grid(row=self.curr_row, column=0)
            Entry(self.setting_frame, width=entry_width, justify='right',
                  textvariable=self.parameters[param]).\
                grid(row=self.curr_row, column=1)
            self.curr_row += 1

        self.reset_button = Button(self.setting_frame, text='Reset',
                                   font=fonts['sub_button'], height=2,
                                   command=self.reset_settings)
        self.reset_button.grid(row=0, column=1)

        self.execute_button = Button(self.setting_frame, text='Execute',
                                     font=fonts['main_button'], height=2,
                                     command=self.execute_warning)
        self.execute_button.grid(row=self.curr_row, column=1)
        self.curr_row += 1

    def init_presets(self):
        """ Initializes widgets related to suggested presets for the
        initial population profile.
        """
        # ----- Presets ----- #
        """" Suggested presets for the initial population profile. 
        The 'all_presets' indexes each preset with its corresponding
        dictionary and Button. The Button starts as None. 
        """

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

        # ----- GUI ----- #
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
        """ Initializes widgets related to matplotlib graph that shows
        simulation results. Starts as an empty graph until simulation
        is executed with 'Execute' Button.
        """
        sample_fig = Figure(figsize=(5, 5), dpi=100)
        a = sample_fig.add_subplot(111)
        a.plot()

        canvas = FigureCanvasTkAgg(sample_fig, self.graph_frame)
        canvas.show()
        canvas.get_tk_widget().grid(row=0, column=1)

    # ----- GUI logic ----- #
    def reset_settings(self):
        for strat_list in self.all_strats.keys():
            for strat in self.all_strats[strat_list].keys():
                self.all_strats[strat_list][strat].set(0)

    def execute_warning(self):
        response = messagebox.askquestion("Confirmation",
                                          "Are you sure you would like to "
                                          "execute this simulation?")
        if response == 'yes':
            self.compile_profile()
            pass

    def compile_profile(self):
        """ Creates a dictionary which describes the initial population using
        the inputted data. Passed to 'run_simulation()' in main.py.
        """
        profile = {}
        for strategy_type in self.all_strats:
            for strategy in self.all_strats[strategy_type]:
                profile[strategy] = self.all_strats[strategy_type][strategy].get()
        return profile

    def select_preset(self, preset):
        pass


    # ----- Simulation logic ----- #
    def execute_plot(self, profile):
        print("creating matplotlib plot")
        pass


# ----- Styling ----- #
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


# ----- Execution ----- #
def run_gui():
    """ Starts the GUI. """

    root = Tk()
    root.title("IPD Simulation")
    root.minsize(1400, 800)
    root.geometry("1400x800")

    ipd = SimulationGUI(root)
    root.mainloop()


if __name__ == '__main__':
    run_gui()
