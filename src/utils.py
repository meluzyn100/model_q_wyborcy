import networkx as nx

def num():
    """Generator liczb całkowitych."""
    i = 0
    while True:
        yield i
        i += 1


def control():
    """Generator kontrolny."""
    c = True
    while True:
        yield c
        c = False


def graph_animate(frame, axs, fig, y, k, N_plus_l, dt, dx):
    """Animacja symulacji grafu"""
    axs[0].clear()
    time = dt * next(k) * dx
    fig.suptitle("Time: {:.2f} MCS".format(time))
    for _ in range(dx):
        G, color_map, N_plus_new = next(y)
        N_plus_l.append(N_plus_new)
    axs[1].plot([time + i * dt for i in range(dx + 1)], N_plus_l, c="green")
    axs[1].plot(
        [time + i * dt for i in range(dx + 1)],
        [1 - index for index in N_plus_l],
        c="red",
    )
    for _ in range(dx):
        N_plus_l.pop(0)

    axs[1].set_ylim([-0.01, 1.01])
    nx.draw_circular(G, ax=axs[0], node_color=color_map, with_labels=True)


def net_animate(frame, axs, fig, y, k, N_plus_l, dt, dx, N, cmap, norm):
    """Animacja symulacji sieci."""
    axs[0].clear()
    time = dt * next(k) * dx
    fig.suptitle("Time: {:.2f} MCS".format(time))

    for _ in range(dx):
        model_now, N_plus_new = next(y)

        N_plus_l.append(N_plus_new / N**2)
    axs[0].pcolor(model_now, cmap=cmap, norm=norm)

    axs[1].plot([time + i * dt for i in range(dx + 1)], N_plus_l, c="green")
    axs[1].plot(
        [time + i * dt for i in range(dx + 1)],
        [1 - index for index in N_plus_l],
        c="red",
    )
    for _ in range(dx):
        N_plus_l.pop(0)

    axs[1].set_ylim([-0.01, 1.01])