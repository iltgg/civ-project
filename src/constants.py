MATERIAL_PROPERTIES = {
    'mat_board': {
        'dimensions': [813, 1016, 1.27],  # mm
        'amount': 0.826008, # m^2
        'tensile_strength': 30,  # Mpa
        'compressive_strength': 6,  # Mpa
        'shear_strength': 4,  # Mpa
        'E': 4000,  # Mpa
        'poisson': 0.2  # unit less
    },
    'contact_cement': {
        'shear_strength': 2  # Mpa
    }
}

PRECISION = 0.001  # three decimal points of precision

TESTING_SETUP ={
    'supports': 50,  # mm, on each side
    'min_span': 1250, # mm
    'max_span': 1270, # mm
    'max_height': 200, # mm
    'max_depth': 200, # mm
    'depth_envelope_angle': 30, # degrees
    'deck_width': 100 # mm
}