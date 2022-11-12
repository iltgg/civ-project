# CIV102 Python Bridge Calculator

George Chen, Benjamin Low, Casey Takahashi

stealing this code is a crime punishable by a fate worse than death (getting a 0)

## Documentation

### deliverable-one.py

Train and Bridge objects provide the needed functionality

Example (inside main):

```python
import matplotlib.pyplot as plt

# t = Train(146, 400) # train in middle of bridge
t = Train(0, 400)  # left-most position, weight
b = Bridge(1200)  # length

# get positions and loads, in extra variables for clarity
wheel_positions = t.get_wheel_positions()
wheel_loads = t.get_point_loads()

shear_force_data = b.calculate_shear_force(wheel_positions, wheel_loads)

bending_moment_data = b.calculate_bending_moment(
    wheel_positions, wheel_loads)

# Plot data
plt.subplot(211)
plt.xlabel('distance (mm)')
plt.ylabel('shear force (N)')
plt.title('Shear Force Diagram')
plt.step(shear_force_data[0], shear_force_data[1], where='post')

plt.subplot(212)
plt.xlabel('distance (mm)')
plt.ylabel('bending moment (Nmm)')
plt.title('Bending Moment Diagram')
plt.gca().invert_yaxis()
plt.plot(bending_moment_data[0], bending_moment_data[1])

plt.tight_layout()
plt.show()
```
