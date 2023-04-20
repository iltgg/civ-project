# CIV102 Python Bridge Calculator

George Chen, Benjamin Low, Casey Takahashi

- [CIV102 Python Bridge Calculator](#civ102-python-bridge-calculator)
  - [bridgeplotlib](#bridgeplotlib)
    - [Quick start](#quick-start)
    - [design-final output](#design-final-output)
  - [bridgeplotlib.py](#bridgeplotlibpy)
    - [geometry\_object](#geometry_object)
    - [geometry\_collection](#geometry_collection)
    - [bridge](#bridge)
    - [train](#train)


## bridgeplotlib

`bridgeplotlib` is a library meant for the structural analysis of a simply supported beam bridge.

### Quick start

See design-0.py or design-final.py for examples

General process:

1. `from bridgeplotlib import *` to use all associated modules
2. Create geometry objects
3. Use geometry objects to create geometry collections, i.e cross sections for bridge
4. Create a cross sections object from the geometry collections
5. Create a bridge object specifying length
6. Solve for max forces at all train locations or a specific train location using `solve_maximum_forces(...)`
7. Display graphs and print FOS and max loads using `display_graphs()`

### design-final output

![main section cross section](/img/main-section.png)
![outer section cross section](/img/outer-section.png)
![diaphragm section cross section](/img/diaphragm-section.png)
![calculation results](/img/results.png)

## bridgeplotlib.py

Contains all functions necessary to graph maximum force and find FOS

### geometry_object

```python
class Rect:
    def __init__(self, x: float, y: float, x_length: float, y_length: float, tags=None, id=None, name=None, join_id=None, special_id=None) -> None:
            """create a geometry object, up is positive and right is positive

                    Args:
                        x (number): top left corner
                        y (number): top left corner
                        x_length (number): x length, right direction
                        y_length (number): y length, down direction
                        tags (str, optional): set a tag for use, format 'ARG1:VALUE1 ARG2:VALUE2 ...'. Defaults to None.
                        id (str, optional): set an id for use, does not need to be unique. Defaults to None.
                        name(str, optional): name of the object
                        join_id (str, optional): special join id, will attach all to all other geometry objects with same join id when a geometry collection is initialized. Only works if all geometry objects are collinear and vertically stacked Joints will be preserved for analysis and display, however the "joined" geometry objects will act as one rect (they are replaced by a new rect with combined dimensions). Defaults to None.
                        special_id (str, optional): special id, for further identification purposes
            """
```

tags:

- display:True
- display:False
- joint-display:True
- joint-display:False

### geometry_collection

```python
class GeometryCollection:
    def __init__(self, geometry_objects: Iterable, geometry_object_groups=(), name=None, ignore_thin_plate=False, joint_override=None) -> None:
            """create a geometry collection object, only supports Rect() geometry objects

            Args:
                geometry_objects (Iterable): an array of geometry_object
                geometry_object_groups (Iterable): (ID, ID, ...), (ID, ID, ...), ...
                name (str, optional): name of the collection
                ignore_thin_plates (bool, optional): True to disable thin plate identification, useful for diaphragms
                joint_override (list, optional): Specify joints that should be used for calculations
            """
```

### bridge

```python
class Bridge:
    def __init__(self, length: int, cross_sections: object) -> None:
        """Initialize a bridge object

        Args:
            length (number): length of the bridge in millimeters
            cross_sections (object): a cross sections object containing bridge cross sections
        """
```

```python
class CrossSections:
    def __init__(self, cross_sections: Iterable, bounds: Iterable, types: Iterable) -> None:
        """create a cross sections object

        Args:
            cross_sections (Iterable): list of cross section
            bounds (Iterable): list of bounds for each cross section
            types (Iterable): list of types for each cross section (diaphragm, ...)
        """
```

### train

```python
class Train:
    def __init__(self, pos, weight) -> None:
        """Initialize a train object

        Args:
            pos (number): left-most position of the train in millimeters
            weight (number): weight of train in newtons
        """
```
