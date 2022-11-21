import matplotlib.pyplot as plt
import numpy as np

from src import bridge, train, geometry_collection, geometry_object, grapher, constants


def display_old(Bridge: object, train_weight, movement_increment):

    # Plot data
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    ax1.set_xlabel('distance (mm)')
    ax1.set_ylabel('shear force (N)')
    ax1.set_title('Shear Force Diagram')
    # ax1.set_xlim(0, Bridge.length)
    ax1.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        shear_force_data = Bridge.calculate_shear_force(
            wheel_positions, wheel_loads)

        ax1.step(shear_force_data[0], shear_force_data[1], where='post')

    ax2.set_xlabel('distance (mm)')
    ax2.set_ylabel('bending moment (Nmm)')
    ax2.set_title('Bending Moment Diagram')
    ax2.invert_yaxis()
    # ax2.set_xlim(0, Bridge.length)
    ax2.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        bending_moment_data = Bridge.calculate_bending_moment(
            wheel_positions, wheel_loads)
        ax2.plot(bending_moment_data[0], bending_moment_data[1])

    fig.tight_layout()
    plt.show()


def plot_bending_moment(Bridge, train_weight, movement_increment, ax):
    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('bending moment (Nmm)')
    ax.set_title('Bending Moment Diagram')
    ax.invert_yaxis()
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


def display(Bridge, train_weight, movement_increment):

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    ax1.set_xlabel('distance (mm)')
    ax1.set_ylabel('shear force (N)')
    ax1.set_title('Shear Force Diagram')
    # ax1.set_xlim(0, Bridge.length)
    ax1.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        shear_force_data = Bridge.calculate_shear_force(
            wheel_positions, wheel_loads)

        ax1.step(shear_force_data[0], shear_force_data[1], where='post')

    ax2.set_xlabel('distance (mm)')
    ax2.set_ylabel('bending moment (Nmm)')
    ax2.set_title('Bending Moment Diagram')
    ax2.invert_yaxis()
    # ax2.set_xlim(0, Bridge.length)
    ax2.hlines(0, 0, Bridge.length, color='grey')
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

        ax2.plot(x, bmd)

    fig.tight_layout()
    plt.show()


def maximum_bending_moment(Bridge, train_weight, movement_increment):
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


def display_max_flexural_stress(Bridge, train):
    fig, ax = plt.subplots(1, 1)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('stress (Mpa)')
    ax.set_title('Flexural Stress')

    ax.hlines(0, 0, Bridge.length, color='grey')

    top = []
    bottom = []

    x = np.linspace(0.01, Bridge.length-0.01, 10_000)

    # get positions and loads, in extra variables for clarity
    # wheel_positions = t.get_wheel_positions()
    # wheel_loads = t.get_point_loads()

    Bridge.solve_shear_force(
        train.get_wheel_positions(), train.get_point_loads())

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

    plot_bending_moment(Bridge, train.weight, 10, ax)

    max_bm = maximum_bending_moment(Bridge, train.weight, 10)
    # remove None hack
    print(
        f'FOS Tension: {max(list(filter(lambda item: item is not None, bottom)))/max_bm}')
    print(
        f'FOS Compression: {max(list(filter(lambda item: item is not None, top)))/max_bm}')

    plt.show()


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
