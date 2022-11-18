import matplotlib.pyplot as plt

from src import bridge, train, geometry_collection, geometry_object, grapher


def display(Bridge: object, train_weight, movement_increment):

    # Plot data
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.set_figheight(5)
    fig.set_figwidth(10)

    ax1.set_xlabel('distance (mm)')
    ax1.set_ylabel('shear force (N)')
    ax1.set_title('Shear Force Diagram')
    ax1.set_xlim(0, Bridge.length)
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
    ax2.set_xlim(0, Bridge.length)
    ax2.hlines(0, 0, Bridge.length, color='grey')
    for i in range(0, 241, movement_increment):
        t = train.Train(i, 800)  # left-most position, weight

        # get positions and loads, in extra variables for clarity
        wheel_positions = t.get_wheel_positions()
        wheel_loads = t.get_point_loads()

        bending_moment_data = Bridge.calculate_bending_moment(
            wheel_positions, wheel_loads)
        ax2.plot(bending_moment_data[0], bending_moment_data[1])

    fig.tight_layout()
    plt.show()
