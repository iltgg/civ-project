import matplotlib.pyplot as plt
import numpy as np
from typing import Iterable

from src import bridge, train, geometry_collection, geometry_object, grapher, constants


def __maximum_bending_moment(Bridge, train_weight, movement_increment):
    maxes = []

    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight
        bmd = []
        x = np.linspace(0.01, Bridge.length-0.01, 10_000)

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        Bridge.solve_shear_force(wheel_positions, wheel_loads)

        for i in x:
            bmd.append(Bridge.get_bending_moment(i))

        maxes.append(max(bmd))

    return max(bmd)


def display_Q(cross_section):
    fig, ax = plt.subplots(1, 1)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    Q = []

    x = np.linspace(cross_section.bottom, cross_section.top, 100_000)

    for i in x:
        Q.append(cross_section.find_Q(i))

    ax.plot(x, Q)

    # ax.text(
    #     0, 7, f'max compression: {min(top)} Mpa\nmax tension: {max(bottom)} Mpa')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    plt.show()


def graph_generic(Bridge, train_weight, movement_increment, ax):
    pass


def graph_sfd(Bridge, train_weight, movement_increment, ax):
    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('shear force (N)')
    ax.set_title('Shear Force Diagram')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)
    # ax1.set_xlim(0, Bridge.length)
    ax.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        shear_force_data = Bridge.calculate_shear_force(
            wheel_positions, wheel_loads)

        ax.step(shear_force_data[0], shear_force_data[1], where='post')


def graph_bmd(Bridge, train_weight, movement_increment, ax):
    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('bending moment (Nmm)')
    ax.set_title('Bending Moment Diagram')
    ax.invert_yaxis()
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)
    # ax2.set_xlim(0, Bridge.length)
    ax.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight
        bmd = []
        x = np.linspace(0.01, Bridge.length-0.01, 10_000)

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        Bridge.solve_shear_force(wheel_positions, wheel_loads)

        for i in x:
            bmd.append(Bridge.get_bending_moment(i))

        ax.plot(x, bmd)


def graph_max_flexural_stress(Bridge, train_weight, movement_increment, ax):
    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('stress (Mpa)')
    ax.set_title('Flexural Stress')

    ax.hlines(0, 0, Bridge.length, color='grey')

    top = []
    bottom = []

    x = np.linspace(0.01, Bridge.length-0.01, 1_200)

    # get positions and loads, in extra variables for clarity
    # wheel_positions = t.get_wheel_positions()
    # wheel_loads = t.get_point_loads()
    t = train.Train(120, 400)

    Bridge.solve_shear_force(
        t.get_wheel_positions(), t.get_point_loads())

    for i in x:
        top.append(Bridge.get_max_force_flexural(
            i, Bridge.cross_sections.get_cross_section(i).top))

    for i in x:
        bottom.append(Bridge.get_max_force_flexural(
            i, Bridge.cross_sections.get_cross_section(i).bottom))

    ax.plot(x, top)
    ax.plot(x, bottom)

    # ax.text(
    #     0, 7, f'max compression: {min(top)} Mpa\nmax tension: {max(bottom)} Mpa')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    graph_bmd(Bridge, t.weight, 10, ax)

    max_bm = __maximum_bending_moment(Bridge, t.weight, 10)
    # remove None hack
    bottom_FOS = max(
        list(filter(lambda item: item is not None, bottom)))/max_bm
    top_FOS = max(list(filter(lambda item: item is not None, top)))/max_bm
    print(
        f'FOS Tension: {bottom_FOS:.3f} | {bottom_FOS*t.weight:.3f}N')
    print(
        f'FOS Compression: {top_FOS:.3f} | {top_FOS*t.weight:.3f}N')


def display_graphs(graphing_functions, rows, cols, size, Bridge, train_weight, movement_increment):

    fig, axes = plt.subplots(rows, cols)
    fig.set_figheight(size*rows)
    fig.set_figwidth(size*cols)

    for i, graph_function in enumerate(graphing_functions):
        axes_pos = __convert_index_to_array_position(i, rows, cols)
        graph_function(Bridge, train_weight, movement_increment,
                       axes[axes_pos[0]][axes_pos[1]])

    fig.tight_layout()

    plt.show()


def __convert_index_to_array_position(i, rows, cols):
    return i % cols, i // cols
