import numpy as np
from  poseProperties import get_trunckVector
from utils.vectors import angle_between

def trunkAngleRecognizer(joints:dict) -> tuple:
    """
    returns true if it has straight truck t[0]
    degrees from straightup 0 = upright -> 180 = upside down t[1]
    """
    trunkVector = get_trunckVector(joints)
    
    up = np.array([0, -1, 0])  # convention

    #  0 = upright -> pi = upside down
    angle = angle_between(up, trunkVector)

    LIMIT = np.pi / 4

    upright = angle < LIMIT

    return (not upright, np.degrees(angle))


    