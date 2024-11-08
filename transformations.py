import numpy as np
from scipy.spatial.transform import Rotation

def transform_positions(positions, xrot=0, xtrans=0, swap=0):
    pos = positions.copy()
    index = 0

    # Permute
    if swap:
        pos[[swap, index]] = pos[[index, swap]]

    # Translate
    if xtrans:
        pos[:, 0] += xtrans

    # Rotate
    if xrot:
        rot = Rotation.from_euler('x', [xrot], degrees=True)
        pos = rot.apply(pos)

    return pos