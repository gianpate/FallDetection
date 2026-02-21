import numpy as np

def angle_between(v1 , v2):
    """Return the angle between v1 and v2 -> rad"""
    dotProduct = np.dot(v1, v2)

    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    cos_theta = dotProduct / (norm_v1 * norm_v2)

    # Clip to [-1, 1] to avoid small errors 
    cos_theta = np.clip(cos_theta, -1.0, 1.0)

    return np.arccos(cos_theta)


def distance(v1, v2):
    return np.linalg.norm(v2 - v1)