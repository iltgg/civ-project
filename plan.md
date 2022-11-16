# Planning


- Perhaps geometry can be defined using “geometry” objects
    - Each rectangle has dimensions and positions
    - Different cross sections can be defined for different portions
    - And total area needed calculated
- For I:
    - Assuming we will only use rectangles (which we will no cylinders)
    - We need (b, h, position) from this the centroid and then I can be found
- For Q:
    - We need (b, h, position, +ability to determine surface area)
    - All of these can be done using the sum of areas and distances
    - “I” should be trivial
    - Q will use much of what I uses however the “b” at any given y is needed. This requires an analysis of the parts of the geometry that are touching
- If a diagonal component will be used, the program must be able to take this into account 

## Geometry object:
- Take size, and position (relative to an origin)
- return area and position
- return area below a certain height
- return local centroid

## Geometry collection:
- return total area below a certain height
- return centroid
- return surface area at given height (more complex will have two values for same height)

- find I and Q

## Solver

### Train - complete

Return loads

### Bridge I - complete

Find shear force

Find bending moment

### Bridge II

Same as bridge I, now implements the geometry

Implement multiple cross sections for different lengths
- splice joints

Calculate total material usage (minimum usage)
- attempt to fit onto the board size?

calculate stresses across entire bridge

identify factors of safety

use multiple train locations

## Grapher

Graph data, transforming into graphable data if necessary
Animation as well