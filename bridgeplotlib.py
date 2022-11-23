import matplotlib.pyplot as plt
import numpy as np
from typing import Iterable

from src import bridge, train, geometry_collection, geometry_object, constants

SUBDIVISIONS = 2000

maximum_shear_forces = []
maximum_bending_moments = []


def solve_maximum_forces(Bridge, train_weight, movement_increment):
    """solve for the maximum forces that a train will impart on a bridge, save in memory

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
    """
    global maximum_shear_forces
    global maximum_bending_moments

    temp_maximum_shear_forces = []
    temp_maximum_bending_moments = []

    for i, val in enumerate(range(0, 241, movement_increment)):
        # make 120, 241, 10000000 to hack to a value
        temp_maximum_shear_forces.append([])
        temp_maximum_bending_moments.append([])

        x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

        t = train.Train(val, train_weight)

        Bridge.solve_shear_force(t.get_wheel_positions(), t.get_point_loads())

        for x_pos in x:
            # counter += 1
            temp_maximum_shear_forces[i].append(Bridge.get_shear_force(x_pos))
            temp_maximum_bending_moments[i].append(
                Bridge.get_bending_moment(x_pos))

    for i in range(len(temp_maximum_shear_forces[0])):
        temp_sf = []
        temp_bm = []

        for j in range(len(temp_maximum_shear_forces)):
            temp_sf.append(temp_maximum_shear_forces[j][i])
            temp_bm.append(temp_maximum_bending_moments[j][i])

        max_sf = max(temp_sf) if abs(max(temp_sf)) > abs(
            min(temp_sf)) else min(temp_sf)
        max_bm = max(temp_bm) if abs(max(temp_bm)) > abs(
            min(temp_bm)) else min(temp_bm)

        maximum_shear_forces.append(max_sf)
        maximum_bending_moments.append(max_bm)


def display_maximum_forces(Bridge):
    global maximum_shear_forces
    global maximum_bending_moments

    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    ax1.plot(x, maximum_shear_forces)
    ax2.plot(x, maximum_bending_moments)

    # ax.text(
    #     0, 7, f'max compression: {min(top)} Mpa\nmax tension: {max(bottom)} Mpa')
    ax1.grid(which='both', linestyle='--', color='grey', alpha=0.5)
    ax2.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    plt.show()


def display_Q(cross_section):
    fig, ax = plt.subplots(1, 1)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    Q = []

    x = np.linspace(cross_section.bottom, cross_section.top, 1_200)

    for i in x:
        Q.append(cross_section.find_Q(i))

    ax.plot(x, Q)

    # ax.text(
    #     0, 7, f'max compression: {min(top)} Mpa\nmax tension: {max(bottom)} Mpa')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    plt.show()


def display_width(cross_section):
    fig, ax = plt.subplots(1, 1)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    b = []

    x = np.linspace(cross_section.bottom, cross_section.top, 10_200)

    for i in x:
        b.append(cross_section.find_width(i))

    ax.plot(x, b)

    # ax.text(
    #     0, 7, f'max compression: {min(top)} Mpa\nmax tension: {max(bottom)} Mpa')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    plt.show()


def graph_generic(Bridge, train_weight, movement_increment, ax):
    pass


def graph_sfd(Bridge, train_weight, movement_increment, ax):
    """shear force diagram

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
        ax (_type_): _description_
    """
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


def __graph_sfd(Bridge, train_weight, movement_increment, ax):
    """shear force diagram, no axis change

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
        ax (_type_): _description_
    """
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
    """bending moment diagram

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
        ax (_type_): _description_
    """
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
        x = np.linspace(0.01, Bridge.length-0.01, 1_200)

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        Bridge.solve_shear_force(wheel_positions, wheel_loads)

        for i in x:
            bmd.append(Bridge.get_bending_moment(i))

        ax.plot(x, bmd)


def __graph_bmd(Bridge, train_weight, movement_increment, ax):
    """bending moment diagram, no axis change

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
        ax (_type_): _description_
    """
    ax.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, train_weight)  # left-most position, weight
        bmd = []
        x = np.linspace(0.01, Bridge.length-0.01, 1_200)

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        Bridge.solve_shear_force(wheel_positions, wheel_loads)

        for i in x:
            bmd.append(Bridge.get_bending_moment(i))

        ax.plot(x, bmd)


def graph_max_flexural(Bridge, train_weight, movement_increment, ax):
    """graph the maximum force from flexing

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
        ax (_type_): _description_
    """
    global maximum_shear_forces
    global maximum_bending_moments

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('bending moment (Nmm)')
    ax.set_title('Flexural Stress')
    ax.invert_yaxis()
    ax.hlines(0, 0, Bridge.length, color='grey')

    top = []
    top_FOS = []
    bottom = []
    bottom_FOS = []

    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

    t = train.Train(120, 400)
    Bridge.solve_shear_force(
        t.get_wheel_positions(), t.get_point_loads())

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_flexural(
            j, Bridge.cross_sections.get_cross_section(j).top)
        top.append(temp)
        if not temp == None:
            top_FOS.append(temp/maximum_bending_moments[i])

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_flexural(
            j, Bridge.cross_sections.get_cross_section(j).bottom)
        bottom.append(temp)
        if not temp == None:
            bottom_FOS.append(temp/maximum_bending_moments[i])

    ax.plot(x, top, label='max top')
    ax.plot(x, bottom, label='max bottom')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    __graph_bmd(Bridge, t.weight, 10, ax)

    # remove None hack
    bottom_FOS = min(list(filter(lambda item: item is not None, bottom_FOS)))
    top_FOS = min(list(filter(lambda item: item is not None, top_FOS)))
    print(

        f'FOS Tension: {bottom_FOS:.3f} | {bottom_FOS*t.weight:.3f}N')
    print(
        f'FOS Compression: {top_FOS:.3f} | {top_FOS*t.weight:.3f}N')


def graph_max_shear(Bridge, train_weight, movement_increment, ax):
    """graph the maximum force from shear

    Args:
        Bridge (_type_): _description_
        train_weight (_type_): _description_
        movement_increment (_type_): _description_
        ax (_type_): _description_
    """
    global maximum_shear_forces
    global maximum_bending_moments

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('Force (N)')
    ax.set_title('Shear Stress')

    ax.hlines(0, 0, Bridge.length, color='grey')

    centroid = []
    centroid_FOS = []

    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)
    t = train.Train(120, 400)

    Bridge.solve_shear_force(
        t.get_wheel_positions(), t.get_point_loads())

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_shear(
            j, Bridge.cross_sections.get_cross_section(j).centroid)
        centroid.append(temp)
        if not temp == None:
            centroid_FOS.append(temp/abs(maximum_shear_forces[i]))

    ax.plot(x, centroid, label='max centroid')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)
    __graph_sfd(Bridge, t.weight, 10, ax)

    # remove None hack
    centroid_FOS = min(
        list(filter(lambda item: item is not None, centroid_FOS)))
    print(
        f'FOS Shear, Centroid: {centroid_FOS:.3f} | {centroid_FOS*t.weight:.3f}N')

    for joint in Bridge.get_unique_joints():  # im sorry for the spaghetti code, this was the only way
        joint_force = []
        joint_FOS = []

        for i, j in enumerate(x):
            bounded = False
            for bound in joint[2]:
                if __return_bounded(j, bound):
                    bounded = True
            if bounded:
                temp = Bridge.get_max_force_shear(
                    j, joint[0], joint[1], 2)
                joint_force.append(temp)
                if not temp == None:
                    joint_FOS.append(temp/abs(maximum_shear_forces[i]))
            else:
                joint_force.append(None)

        ax.plot(x, joint_force, label=f'max joint {joint[3]} y={joint[0]}')

        # remove None hack
        joint_FOS = min(
            list(filter(lambda item: item is not None, joint_FOS)))
        print(
            f'FOS Shear, Joint {joint[3]} y={joint[0]}: {joint_FOS:.3f} | {joint_FOS*t.weight:.3f}N')


def __return_bounded(x: float, bound: Iterable) -> bool:
    """return if the x is within a bound

    Args:
        x (number): an x value
        bound (Iterable): a bound in the from (a, b)

    Returns:
        bool: True if x is within the bound
    """
    if x >= bound[0] and x <= bound[1]:
        return True
    else:
        return False


def display_graphs(graphing_functions, rows, cols, size, Bridge, train_weight, movement_increment):

    fig, axes = plt.subplots(rows, cols)
    fig.set_figheight(size*rows)
    fig.set_figwidth(size*cols)

    for i, graph_function in enumerate(graphing_functions):
        axes_pos = __convert_index_to_array_position(i, rows, cols)
        graph_function(Bridge, train_weight, movement_increment,
                       axes[axes_pos[0]][axes_pos[1]])

    fig.legend()
    fig.tight_layout()

    plt.show()


def __convert_index_to_array_position(i, rows, cols):
    return i % cols, i // cols
