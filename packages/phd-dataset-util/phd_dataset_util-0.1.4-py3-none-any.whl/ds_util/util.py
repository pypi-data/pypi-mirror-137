import numpy as np

def get_nearest_value(sim_values,value):
    """
        Given a value and a values list this method return from the the nearest element to the value
    """
    absolute_val_array = np.abs(sim_values - value)
    return sim_values[absolute_val_array.argmin()]