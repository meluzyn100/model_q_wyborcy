import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from src.simulations import gen, loopinf
from src.utils import num, graph_animate, net_animate
import networkx as nx
import numpy as np


def gui():
    """Interfejs graficzny aplikacji."""
    root = tk.Tk()

    root.attributes("-zoomed", True)  # .attributes
    for i in range(25):
        root.rowconfigure(i, weight=1, minsize=20)
    for i in range(6):
        root.columnconfigure(i, weight=1, minsize=20)

    root.columnconfigure(4, weight=0)
    root.title("Model q-wyborcy")

    label2 = tk.Label(text="N:")
    label2.config(font=("Comic Sans MS", 15))
    label2.grid(row=1, column=1, sticky="e")

    label3 = tk.Label(text="N_+(0):")
    label3.config(font=("Comic Sans MS", 15))
    label3.grid(row=2, column=1, sticky="e")

    label4 = tk.Label(text="q:")
    label4.config(font=("Comic Sans MS", 15))
    label4.grid(row=3, column=1, sticky="e")

    label5 = tk.Label(text="p:")
    label5.config(font=("Comic Sans MS", 15))
    label5.grid(row=4, column=1, sticky="e")

    label6 = tk.Label(text="f:")
    label6.config(font=("Comic Sans MS", 15))
    label6.grid(row=5, column=1, sticky="e")

    label7 = tk.Label(text="dt:")
    label7.config(font=("Comic Sans MS", 15))
    label7.grid(row=6, column=1, sticky="e")

    label7 = tk.Label(text="T:")
    label7.config(font=("Comic Sans MS", 15))
    label7.grid(row=7, column=1, sticky="e")

    cb_label = tk.Label(text="Wersji nonkonformizmu", font=("Comic Sans MS", 15))
    cb_label.grid(row=8, column=1, columnspan=2, sticky="s")
    choices1 = ("niezależność", "antykonformizm")
    choiceVar1 = tk.StringVar()
    choiceVar1.set(choices1[0])
    cb1 = ttk.Combobox(
        root, textvariable=choiceVar1, values=choices1, font=("Comic Sans MS", 15)
    )
    cb1.grid(row=9, column=1, columnspan=2, sticky="n")
    cb_label = tk.Label(text="Typ losowania", font=("Comic Sans MS", 15))
    cb_label.grid(row=10, column=1, columnspan=2, sticky="s")

    choices2 = ("powtórzenia", "bezpowtórzen")
    choiceVar2 = tk.StringVar()
    choiceVar2.set(choices2[0])
    cb2 = ttk.Combobox(
        root, textvariable=choiceVar2, values=choices2, font=("Comic Sans MS", 15)
    )
    cb2.grid(row=11, column=1, columnspan=2, sticky="n")

    cb_label = tk.Label(text="Graf/siatka", font=("Comic Sans MS", 15))
    cb_label.grid(row=12, column=1, columnspan=2, sticky="s")
    choices3 = ("graf", "siatka")
    choiceVar3 = tk.StringVar()
    choiceVar3.set(choices3[0])
    cb3 = ttk.Combobox(
        root, textvariable=choiceVar3, values=choices3, font=("Comic Sans MS", 15)
    )
    cb3.grid(row=13, column=1, columnspan=2, sticky="n")

    entry_text1 = tk.StringVar()
    e1 = tk.Entry(textvariable=entry_text1)
    entry_text1.set("20")
    e1.config(font=("Comic Sans MS", 15))
    e1.grid(row=1, column=2)

    entry_text2 = tk.StringVar()
    e2 = tk.Entry(textvariable=entry_text2)
    entry_text2.set("10")
    e2.config(font=("Comic Sans MS", 15))
    e2.grid(row=2, column=2)

    entry_text3 = tk.StringVar()
    e3 = tk.Entry(textvariable=entry_text3)
    entry_text3.set("3")
    e3.config(font=("Comic Sans MS", 15))
    e3.grid(row=3, column=2)

    entry_text4 = tk.StringVar()
    e4 = tk.Entry(textvariable=entry_text4)
    entry_text4.set("0.1")
    e4.config(font=("Comic Sans MS", 15))
    e4.grid(row=4, column=2)

    entry_text5 = tk.StringVar()
    e5 = tk.Entry(textvariable=entry_text5)
    entry_text5.set("0.5")
    e5.config(font=("Comic Sans MS", 15))
    e5.grid(row=5, column=2)

    entry_text6 = tk.StringVar()
    e6 = tk.Entry(textvariable=entry_text6)
    entry_text6.set("1")
    e6.config(font=("Comic Sans MS", 15))
    e6.grid(row=6, column=2)

    entry_text6 = tk.StringVar()
    e7 = tk.Entry(textvariable=entry_text6)
    entry_text6.set("Inf")
    e7.config(font=("Comic Sans MS", 15))
    e7.grid(row=7, column=2)

    label_end2 = tk.Label(text="N - rozmiar układu")
    label_end2.config(font=("Comic Sans MS", 15))
    label_end2.grid(row=17, column=1, columnspan=3, sticky="w")

    label_end3 = tk.Label(text="N_+(0) - początkowa ilość pozytywnych agentów")
    label_end3.config(font=("Comic Sans MS", 15))
    label_end3.grid(row=18, column=1, columnspan=3, sticky="w")

    label_ene4 = tk.Label(text="q - rozmiar grupy wpływu")
    label_ene4.config(font=("Comic Sans MS", 15))
    label_ene4.grid(row=19, column=1, columnspan=3, sticky="w")

    label_ene5 = tk.Label(text="p - prawdopodobieństwo niezależności/antykonformizmu")
    label_ene5.config(font=("Comic Sans MS", 15))
    label_ene5.grid(row=20, column=1, columnspan=3, sticky="w")

    label_ene6 = tk.Label(text="f - w niezależności prawdopodobieństwo bycia na nie ")
    label_ene6.config(font=("Comic Sans MS", 15))
    label_ene6.grid(row=21, column=1, columnspan=3, sticky="w")

    label_ene7 = tk.Label(
        text="dt - co ile elementarnych kroków czasowych wyświetlany jest układ (parametr szybkości wyświetlania)"
    )
    label_ene7.config(font=("Comic Sans MS", 15))
    label_ene7.grid(row=22, column=1, columnspan=3, sticky="w")

    label_ene8 = tk.Label(text="T - czas symulacji (inf - nieskączoność)")
    label_ene8.config(font=("Comic Sans MS", 15))
    label_ene8.grid(row=23, column=1, columnspan=3, sticky="w")

    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().grid(column=3, row=2, rowspan=6)

    def start_anim():
        axs[1].set_xlabel("t[MCS]")
        axs[1].set_ylabel("c")

        N = int(e1.get())
        N_plus = int(e2.get())
        N_minus = N - N_plus
        q = int(e3.get())
        p = float(e4.get())
        f_p = float(e5.get())
        dx = int(e6.get())

        if cb1.get() == "niezależność":
            independene = True
        else:
            independene = False

        if cb2.get() == "powtórzenia":
            type_of_choosing = True
        else:
            type_of_choosing = False

        if cb3.get() == "graf":
            graf = True
        else:
            graf = False

        if e7.get().lower() == "inf":
            inf_time = True
            T = 1
        else:
            T = float(e7.get())
            inf_time = False

        if graf:
            nr_of_i = int(T * N / dx)
            dt = 1 / N
        else:
            nr_of_i = int(T * N**2 / dx)
            dt = 1 / N**2

        if graf:
            N_plus_l = [N_plus / N]

            data = np.array([1] * N_plus + [-1] * N_minus)
            np.random.shuffle(data)

            G = nx.Graph()
            G.add_nodes_from(range(N))

            y = gen(N, N_plus, N_minus, p, q, f_p, type_of_choosing, independene)
            k = num()

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.get_tk_widget().grid(column=3, row=1, rowspan=7)

            if inf_time:
                ani = animation.FuncAnimation(
                    fig,
                    graph_animate,
                    interval=1,
                    blit=False,
                    fargs=(axs, fig, y, k, N_plus_l, dt, dx),
                )

            else:
                ani = animation.FuncAnimation(
                    fig,
                    graph_animate,
                    frames=range(nr_of_i),
                    interval=1,
                    blit=False,
                    repeat=False,
                    fargs=(axs, fig, y, k, N_plus_l, dt, dx),
                )

        else:
            N_plus_l = [N_plus / N**2]

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
            y = loopinf(N, index, model, q, type_of_choosing, independene, p, f_p)
            k = num()

            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.get_tk_widget().grid(column=3, row=1, rowspan=7)

            if inf_time:
                ani = animation.FuncAnimation(
                    fig,
                    net_animate,
                    interval=1,
                    blit=False,
                    fargs=(axs, fig, y, k, N_plus_l, dt, dx, N, cmap, norm),
                )

            else:
                ani = animation.FuncAnimation(
                    fig,
                    net_animate,
                    frames=range(nr_of_i),
                    interval=1,
                    blit=False,
                    repeat=False,
                    fargs=(axs, fig, y, k, N_plus_l, dt, dx, N, cmap, norm),
                )

        def stop_anim():
            ani.event_source.stop()

        def resum_anim():
            ani.event_source.start()

        def reset_all():
            ani.event_source.stop()
            axs[0].clear()
            axs[1].clear()
            start_anim()

        b2 = tk.Button(text="Stop", command=stop_anim)
        b2.config(font=("Comic Sans MS", 20))
        b2.grid(row=15, column=2, sticky="ew")

        b4 = tk.Button(text="Restart", command=reset_all)
        b4.config(font=("Comic Sans MS", 20))
        b4.grid(row=16, column=1, sticky="ew")

        b3 = tk.Button(text="Resume", command=resum_anim)
        b3.config(font=("Comic Sans MS", 20))
        b3.grid(row=16, column=2, sticky="ew")

        b1 = tk.Button(text="Start", command=reset_all)
        b1.config(font=("Comic Sans MS", 20))
        b1.grid(row=15, column=1, sticky="ew")

        root.update()

    b1 = tk.Button(text="Start", command=start_anim)
    b1.config(font=("Comic Sans MS", 20))
    b1.grid(row=15, column=1, sticky="ew")
    b1.grid(row=15, column=1, sticky="ew")

    tk.mainloop()
