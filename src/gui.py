import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from src.simulations import gen, loopinf
from src.utils import num, graph_animate, net_animate
import numpy as np


def create_labels(root):
    """Create and place labels in the GUI."""
    labels = [
        ("N:", 1),
        ("N_+(0):", 2),
        ("q:", 3),
        ("p:", 4),
        ("f:", 5),
        ("dt:", 6),
        ("T:", 7),
    ]
    for text, row in labels:
        label = tk.Label(text=text, font=("Comic Sans MS", 15))
        label.grid(row=row, column=1, sticky="e")

    # Additional labels for explanations
    explanations = [
        ("N - rozmiar układu", 17),
        ("N_+(0) - początkowa ilość pozytywnych agentów", 18),
        ("q - rozmiar grupy wpływu", 19),
        ("p - prawdopodobieństwo niezależności/antykonformizmu", 20),
        ("f - w niezależności prawdopodobieństwo bycia na nie", 21),
        (
            "dt - co ile elementarnych kroków czasowych wyświetlany jest układ (parametr szybkości wyświetlania)",
            22,
        ),
        ("T - czas symulacji (inf - nieskończoność)", 23),
    ]
    for text, row in explanations:
        label = tk.Label(text=text, font=("Comic Sans MS", 15))
        label.grid(row=row, column=1, columnspan=3, sticky="w")


def create_comboboxes(root):
    """Create and place comboboxes in the GUI."""
    combobox_data = [
        ("Wersji nonkonformizmu", ["niezależność", "antykonformizm"], 8, 9),
        ("Typ losowania", ["powtórzenia", "bezpowtórzen"], 10, 11),
        ("Graf/siatka", ["graf", "siatka"], 12, 13),
    ]
    combobox_vars = []
    for label_text, choices, label_row, combo_row in combobox_data:
        label = tk.Label(text=label_text, font=("Comic Sans MS", 15))
        label.grid(row=label_row, column=1, columnspan=2, sticky="s")

        var = tk.StringVar(value=choices[0])
        combobox = ttk.Combobox(
            root, textvariable=var, values=choices, font=("Comic Sans MS", 15)
        )
        combobox.grid(row=combo_row, column=1, columnspan=2, sticky="n")
        combobox_vars.append(var)

    return combobox_vars


def create_entries(root):
    """Create and place entry fields in the GUI."""
    default_values = ["20", "10", "3", "0.1", "0.5", "1", "Inf"]
    entry_vars = []
    for i, default in enumerate(default_values, start=1):
        var = tk.StringVar(value=default)
        entry = tk.Entry(root, textvariable=var, font=("Comic Sans MS", 15))
        entry.grid(row=i, column=2)
        entry_vars.append(var)

    return entry_vars


def create_buttons(
    root, start_callback, stop_callback, resume_callback, reset_callback
):
    """Create and place buttons in the GUI."""
    buttons = [
        ("Start", start_callback, 15, 1),
        ("Stop", stop_callback, 15, 2),
        ("Resume", resume_callback, 16, 2),
        ("Restart", reset_callback, 16, 1),
    ]
    for text, command, row, column in buttons:
        button = tk.Button(text=text, command=command, font=("Comic Sans MS", 20))
        button.grid(row=row, column=column, sticky="ew")


def gui():
    """Interfejs graficzny aplikacji."""
    root = tk.Tk()
    root.attributes("-zoomed", True)  # .attributes
    root.title("Model q-wyborcy")

    for i in range(25):
        root.rowconfigure(i, weight=1, minsize=20)
    for i in range(6):
        root.columnconfigure(i, weight=1, minsize=20)
    root.columnconfigure(4, weight=0)

    create_labels(root)
    combobox_vars = create_comboboxes(root)
    entry_vars = create_entries(root)

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=3, row=2, rowspan=6)

    def start_animation():
        """Start the animation based on user inputs."""
        axs[1].set_xlabel("t[MCS]")
        axs[1].set_ylabel("c")

        N = int(entry_vars[0].get())
        N_plus = int(entry_vars[1].get())
        q = int(entry_vars[2].get())
        p = float(entry_vars[3].get())
        f_p = float(entry_vars[4].get())
        dx = int(entry_vars[5].get())
        T = entry_vars[6].get()
        inf_time = T.lower() == "inf"
        T = float(T) if not inf_time else 1

        # Retrieve combobox values
        independence = combobox_vars[0].get() == "niezależność"
        type_of_choosing = combobox_vars[1].get() == "powtórzenia"
        is_graph = combobox_vars[2].get() == "graf"

        # Calculate parameters
        N_minus = N - N_plus
        dt = 1 / (N if is_graph else N**2)
        nr_of_iterations = int(T * (N if is_graph else N**2) / dx)
        N_plus_l = [N_plus / (N if is_graph else N**2)]

        if is_graph:
            y = gen(N, N_plus, N_minus, p, q, f_p, type_of_choosing, independence)
            k = num()

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.get_tk_widget().grid(column=3, row=1, rowspan=7)

            ani = animation.FuncAnimation(
                fig,
                graph_animate,
                frames=range(nr_of_iterations) if not inf_time else None,
                interval=1,
                blit=False,
                repeat=False if not inf_time else None,
                fargs=(axs, fig, y, k, N_plus_l, dt, dx),
            )

        else:
            cmap = colors.ListedColormap(["red", "green"])
            bounds = [-1.5, 0, 1.5]
            norm = colors.BoundaryNorm(bounds, cmap.N)
            n = N
            m_dim = n
            ones_n = N_plus
            index = [n - 1] + [i for i in range(n)] + [0]

            nimus_ones_n = n * m_dim - ones_n
            onli_ones = np.ones(ones_n)
            onli_minus_ones = -1 * np.ones(nimus_ones_n)
            model = np.concatenate([onli_ones, onli_minus_ones])
            np.random.shuffle(model)
            model = model.reshape(n, m_dim)
            y = loopinf(N, index, model, q, type_of_choosing, independence, p, f_p)
            k = num()

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.get_tk_widget().grid(column=3, row=1, rowspan=7)

            ani = animation.FuncAnimation(
                fig,
                net_animate,
                frames=range(nr_of_iterations) if not inf_time else None,
                interval=1,
                blit=False,
                repeat=False if not inf_time else None,
                fargs=(axs, fig, y, k, N_plus_l, dt, dx, N, cmap, norm),
            )

        def stop_animation():
            ani.event_source.stop()

        def resume_animation():
            ani.event_source.start()

        def reset_animation():
            try:
                ani.event_source.stop()
            except AttributeError:
                pass
            axs[0].clear()
            axs[1].clear()
            start_animation()

        create_buttons(
            root, start_animation, stop_animation, resume_animation, reset_animation
        )

        root.update()

    create_buttons(root, start_animation, None, None, None)
    tk.mainloop()
