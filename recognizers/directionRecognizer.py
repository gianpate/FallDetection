import numpy as np
from utils.vectors import angle_between

def get_PoseDirection(joints:dict):
    head = np.array(joints["head"])
    rightShoulder = np.array(joints["right_shoulder"])
    leftShoulder = np.array(joints["left_shoulder"])

    head_left =  leftShoulder - head
    head_right = rightShoulder - head

    direction = np.cross(head_left, head_right)

    return direction



def directionRecognizer(joints:dict) -> tuple:
    """
    returns true if it doesnt looks straight t[0]
    degrees from straightus up~+90 and down~-90 t[1]
    """

    direction = get_PoseDirection(joints)
    up = np.array([0, -1, 0])  # convention

    angle = angle_between(up, direction)

    LOWER_LIMIT = np.pi / 4
    UPPER_LIMIT = 3 * np.pi / 4
    STRAIGHT = np.pi / 2

    # check if pose faces straight
    looks_straight = LOWER_LIMIT <= angle <= UPPER_LIMIT

    # calculate slope from straight
    slope = np.degrees(STRAIGHT - angle)

    return (not looks_straight, slope)

    

