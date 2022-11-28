import matplotlib.pyplot as plt
import numpy as np
from typing import Iterable

from src import bridge, train, geometry_collection, geometry_object, constants

SUBDIVISIONS = 2000

maximum_shear_forces = []
maximum_bending_moments = []


def solve_maximum_forces(Bridge, train_weight=400, movement_increment=10, single_position=None):
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

    if single_position:
        i = 0
        val = single_position
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
    else:
        for i, val in enumerate(range(0, 241, movement_increment)):
            # make 120, 241, 10000000 to hack to a value
            temp_maximum_shear_forces.append([])
            temp_maximum_bending_moments.append([])

            x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

            t = train.Train(val, train_weight)

            Bridge.solve_shear_force(
                t.get_wheel_positions(), t.get_point_loads())

            for x_pos in x:
                # counter += 1
                temp_maximum_shear_forces[i].append(
                    Bridge.get_shear_force(x_pos))
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


def __graph_sfd_envelope(Bridge, ax):
    """graph the shear force envelope on a given axis

    Args:
        Bridge (object): Bridge object
        ax (object): matplotlib axis
    """
    global maximum_shear_forces
    global maximum_bending_moments

    abs_sfd = []
    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

    for i in maximum_shear_forces:
        abs_sfd.append(abs(i))

    ax.plot(x, abs_sfd, 'r', label='shear force envelope')


def __graph_bmd_envelope(Bridge, ax):
    """graph the bending moment envelope on a given axis

    Args:
        Bridge (object): Bridge object
        ax (object): matplotlib axis
    """
    global maximum_shear_forces
    global maximum_bending_moments

    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

    ax.plot(x, maximum_bending_moments, 'b', label='bending moment envelope')


def graph_max_flexural(Bridge, train_weight, movement_increment, ax):
    """graph the maximum force from flexural stress

    Args:
        Bridge (object): Bridge object
        train_weight (number): weight of the train
        movement_increment (int): how much to move the train
        ax (object): matplotlib axis
    """
    global maximum_shear_forces
    global maximum_bending_moments

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('bending moment (Nmm)')
    ax.set_title('Max Flexural Force')
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

    ax.plot(x, top, label='max force top')
    ax.plot(x, bottom, label='max force bottom')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    # __graph_bmd(Bridge, t.weight, 10, ax)
    __graph_bmd_envelope(Bridge, ax)
    # ax.legend(loc='upper right')
    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    # remove None hack
    bottom_FOS = min(list(filter(lambda item: item is not None, bottom_FOS)))
    top_FOS = min(list(filter(lambda item: item is not None, top_FOS)))
    print(

        f'FOS Tension: {bottom_FOS:.3f} | {bottom_FOS*t.weight:.3f}N')
    print(
        f'FOS Compression: {top_FOS:.3f} | {top_FOS*t.weight:.3f}N')


def graph_max_shear(Bridge, train_weight, movement_increment, ax):
    """graph the maximum force from shear stress

    Args:
        Bridge (object): Bridge object
        train_weight (number): weight of the train
        movement_increment (int): how much to move the train
        ax (object): matplotlib axis
    """
    global maximum_shear_forces
    global maximum_bending_moments

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('Force (N)')
    ax.set_title('Max Shear Force')

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

    ax.plot(x, centroid, 'k', label='max force centroid')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)
    # __graph_sfd(Bridge, t.weight, 10, ax)

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

        ax.plot(x, joint_force,
                label=f'max force glue joint {joint[3]} y={joint[0]}')

        # remove None hack
        joint_FOS = min(
            list(filter(lambda item: item is not None, joint_FOS)))
        print(
            f'FOS Shear, Glue Joint {joint[3]} y={joint[0]}: {joint_FOS:.3f} | {joint_FOS*t.weight:.3f}N')
    # ax.legend(loc='upper right')
    __graph_sfd_envelope(Bridge, ax)
    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")


def graph_max_thin_plate_buckling(Bridge, train_weight, movement_increment, ax):
    """graph the maximum force from thin plate buckling

    Args:
        Bridge (object): Bridge object
        train_weight (number): weight of the train
        movement_increment (int): how much to move the train
        ax (object): matplotlib axis
    """
    global maximum_shear_forces
    global maximum_bending_moments

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('bending moment (Nmm)')
    ax.set_title('Max Thin Plate Buckling')
    ax.invert_yaxis()
    ax.hlines(0, 0, Bridge.length, color='grey')

    top = []
    top_FOS = []
    side = []
    side_FOS = []
    vertical = []
    vertical_FOS = []

    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

    t = train.Train(120, 400)
    Bridge.solve_shear_force(
        t.get_wheel_positions(), t.get_point_loads())

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_tpb_top_flange(j)
        top.append(temp)
        if not temp == None:
            top_FOS.append(temp/maximum_bending_moments[i])

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_tpb_side_flange(j)
        side.append(temp)
        if not temp == None:
            side_FOS.append(temp/maximum_bending_moments[i])

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_tpb_vertical_flange(j)
        vertical.append(temp)
        if not temp == None:
            vertical_FOS.append(temp/maximum_bending_moments[i])

    ax.plot(x, top, label='max force k=4')
    ax.plot(x, side, label='max force k=0.425')
    ax.plot(x, vertical, label='max force k=6')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    # __graph_bmd(Bridge, t.weight, 10, ax)
    __graph_bmd_envelope(Bridge, ax)
    # ax.legend(loc='upper right')
    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    # remove None hack
    top_FOS = min(list(filter(lambda item: item is not None, top_FOS)))
    side_FOS = min(list(filter(lambda item: item is not None, side_FOS)))
    vertical_FOS = min(
        list(filter(lambda item: item is not None, vertical_FOS)))
    print(
        f'FOS Thin Plate Buckling k=4: {top_FOS:.3f} | {top_FOS*t.weight:.3f}N')
    print(
        f'FOS Thin Plate Buckling k=0.425: {side_FOS:.3f} | {side_FOS*t.weight:.3f}N')
    print(
        f'FOS Thin Plate Buckling k=6: {vertical_FOS:.3f} | {vertical_FOS*t.weight:.3f}N')


def graph_max_thin_plate_shear(Bridge, train_weight, movement_increment, ax):
    """graph the maximum force from thin plate shear buckling

    Args:
        Bridge (object): Bridge object
        train_weight (number): weight of the train
        movement_increment (int): how much to move the train
        ax (object): matplotlib axis
    """
    global maximum_shear_forces
    global maximum_bending_moments

    ax.set_xlabel('distance (mm)')
    ax.set_ylabel('force (N)')
    ax.set_title('Max Thin plate Shear Buckling')
    ax.hlines(0, 0, Bridge.length, color='grey')

    side = []
    side_FOS = []

    x = np.linspace(0.01, Bridge.length-0.01, SUBDIVISIONS)

    t = train.Train(120, 400)
    Bridge.solve_shear_force(
        t.get_wheel_positions(), t.get_point_loads())

    for i, j in enumerate(x):
        temp = Bridge.get_max_force_tps(j)
        side.append(temp)
        if not temp == None:
            side_FOS.append(abs(temp/maximum_shear_forces[i]))

    ax.plot(x, side, label='max force k=5')
    ax.grid(which='both', linestyle='--', color='grey', alpha=0.5)

    # __graph_bmd(Bridge, t.weight, 10, ax)
    __graph_sfd_envelope(Bridge, ax)
    # ax.legend(loc='upper right')
    ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")

    # remove None hack
    side_FOS = min(list(filter(lambda item: item is not None, side_FOS)))
    print(
        f'FOS Thin Plate Shear k=5: {side_FOS:.3f} | {side_FOS*t.weight:.3f}N')


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


def display_graphs(graphing_functions: Iterable, rows: int, cols: int, size: float, Bridge: object, train_weight: float, movement_increment: int):
    """display the graphs given in a subplot figure

    Args:
        graphing_functions (Iterable): list of graphing function
        rows (int): how many subplot rows to use
        cols (int): how many subplot columns to use
        size (float): size of each subplot
        Bridge (object): Bridge object
        train_weight (float): weight of the train
        movement_increment (int): how much to move the train
    """
    fig, axes = plt.subplots(rows, cols)
    fig.set_figheight(size*rows)
    fig.set_figwidth(size*cols*2)

    for i, graph_function in enumerate(graphing_functions):
        axes_pos = __convert_index_to_array_position(i, rows, cols)
        # print(axes_pos)
        graph_function(Bridge, train_weight, movement_increment,
                       axes[axes_pos[1]][axes_pos[0]])

    fig.tight_layout(w_pad=1)
    plt.show()


def __convert_index_to_array_position(i: int, rows: int, cols: int) -> tuple:
    """convert the index of an array to the coordinates in a grid of given rows and columns

    Args:
        i (int): index
        rows (int): rows
        cols (int): columns

    Returns:
        (int, int): coords
    """
    return i % cols, i // cols
