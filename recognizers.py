"""
Recognizers for fall detection.

recognizer(joints:dict) -> (bool, float)

    - `bool` : `True` if the recognizer detects the characteristic/fall, `False` otherwise.
    - `float`: a continuous value-index related to the recognized characteristic

Recognizer functions follow the naming pattern `*Recognizer`. The module
provides a function `get_recognizers()` that returns a list of all such
functions defined in this module.
"""


import numpy as np
from utils.vectors import angle_between, distance
import poseProperties as ps


def get_recognizers() -> list:
    """
    Return a list of all recognizer functions defined in this module.
    Recognizer functions are those whose names end with 'Recognizer'
    and are defined directly in this module (not imported)
    """
    import inspect
    import sys
    module = sys.modules[__name__]
    recognizers = []
    for name, obj in inspect.getmembers(module):
        # Only take functions defined in this module, ending with 'Recognizer'
        if (name.endswith('Recognizer') and 
            inspect.isfunction(obj) and 
            obj.__module__ == __name__):
            recognizers.append(obj)
    return recognizers



def directionRecognizer(joints:dict) -> tuple:
    """
    returns true if it doesnt looks straight t[0]
    degrees from straight up~+90 and down~-90 t[1]
    """

    direction = ps.get_PoseDirection(joints)
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

    


def pelvisDownRecognizer(joints:dict) -> tuple:
    """
    returns true if pelvis lower than the height of the knee t[0]
    how far up and down from straight up t[1]:
        - 100%    down
        - 0%      upright
        - >100%   pelvis below feet 
    """
    pelvis = np.array(joints["pelvis"])

    shin = ps.get_shinLength(joints)
    leg = ps.get_legLength(joints)

    feetLevel = ps.get_feetLevel(joints)

    feet_Y = feetLevel[1]
    pelvis_Y = pelvis[1]

    #  -y => up so we subtract
    pelvisHeightLimit = feet_Y - shin 
    
    fall = pelvis_Y > pelvisHeightLimit

    raw_percentageHeight =  100 + (pelvis_Y - feet_Y) / leg * 100
    heightDifFromPelvis = max(0, raw_percentageHeight)

    return (fall, heightDifFromPelvis)




def handsDownRecognizer(joints:dict) -> tuple:
    """
    returns true if hands lower than the height of the knee t[0]
    how far up and down from head (if upright) t[1]:
        - 100%    down
        - 0%      up
        - >100%   hands below feet
        - <0%     hands above head
    """
    feetLevel = ps.get_feetLevel(joints)
    handsLevel = ps.get_handsLevel(joints)

    feet_Y = feetLevel[1]
    hands_Y = handsLevel[1]

    shin = ps.get_shinLength(joints)
    #  -y => up so we subtract
    handsHeightLimit = feet_Y - shin 

    fall = hands_Y > handsHeightLimit

    personHeight = ps.get_personHeight(joints)
    heightDifFromHands = 100 + (hands_Y - feet_Y) / personHeight * 100

    return (fall, heightDifFromHands)




def spanRecognizer(joints:dict) -> tuple:
    """
    returns true if horizontal span exceeds vertical span t[0]
    horizontal span as a percentage of vertical span t[1]:
        - 100%    equal spans
        - >100%   wider than tall
        - <100%   taller than wide
    """
    
    maxY = max(j[1] for j in joints.values())
    minY = min(j[1] for j in joints.values())

    maxX = max(j[0] for j in joints.values())
    minX = min(j[0] for j in joints.values())
    maxZ = max(j[2] for j in joints.values())
    minZ = min(j[2] for j in joints.values())

    # We define span in the XZ as the 
    # distance between (maxX, maxZ) -> (minX, minZ)
    maximum = np.array([maxX, maxZ])
    minimum = np.array([minX, minZ])
    horizontalSpan = distance(maximum, minimum)

    delta_Y = abs(maxY - minY)

    fallSpan = horizontalSpan > delta_Y * 1.5

    percentageOfDeltaY = horizontalSpan / delta_Y * 100

    return (fallSpan, percentageOfDeltaY)




def trunkAngleRecognizer(joints:dict) -> tuple:
    """
    returns true if it has straight truck t[0]
    degrees from straightup 0 = upright -> 180 = upside down t[1]
    """
    trunkVector = ps.get_trunckVector(joints)
    
    up = np.array([0, -1, 0])  # convention

    #  0 = upright -> pi = upside down
    angle = angle_between(up, trunkVector)

    LIMIT = np.pi / 4

    upright = angle < LIMIT

    return (not upright, np.degrees(angle))




def kneesDownRecognizer(joints:dict) -> tuple:
    """
    returns true if knees are lower than ~80% of shin height above feet t[0]
    how high knees are relative to shin length t[1]:
        - 100%    knees straight up
        - 0%      knees at feet level
        - <0%     knees below feet
    """
    feetLevel = ps.get_feetLevel(joints)
    feet_Y = feetLevel[1]

    kneesLevel = ps.get_kneesLevel(joints)
    knees_Y = kneesLevel[1]

    shin = ps.get_shinLength(joints)
    #  -y => up so we subtract
    kneesHeightLimit = feet_Y - shin * 0.8

    fall = knees_Y > kneesHeightLimit

    heightOfKnees = (feet_Y - knees_Y) / shin * 100

    return (fall, heightOfKnees)




def headDownRecognizer(joints:dict) -> tuple:
    """
    returns true if head is lower than the height of the back t[0]
    how low the head is relative to the back height t[1]:
        - >100%   head above threshold (safe upright posture)
        - 100%    head exactly at threshold
        - 0%      head at feet level
        - <0%     head below feet
    """
    head = np.array(joints["head"])
    head_Y = head[1]

    feetLevel = ps.get_feetLevel(joints)
    feet_Y = feetLevel[1]

    backHeight = ps.get_headToPelvisHeight(joints)

    #  -y => up so we subtract
    headHeightLimit = feet_Y - backHeight

    fall = head_Y > headHeightLimit

    heightOfHead = (feet_Y - head_Y) / backHeight * 100

    return (fall, heightOfHead)




def pelvisBelowKneesRecognizer(joints:dict) -> tuple:
    """
    returns true if pelvis is lower than 80% of thigh height above knees t[0]
    how high the pelvis is relative to the knees normalized by thigh length t[1]:
        - >80%   pelvis above threshold (safe upright posture)
        - 80%    pelvis exactly at threshold
        - 0%     pelvis at knee level
        - <0%    pelvis below knees
    """
    pelvis = np.array(joints["pelvis"])
    pelvis_Y = pelvis[1]

    kneesLevel = ps.get_kneesLevel(joints)
    knees_Y = kneesLevel[1]

    thigh = ps.get_thighLength(joints)

    #  -y => up so we subtract
    pelvisHeightLimit = knees_Y - thigh * 0.8

    fall = pelvis_Y > pelvisHeightLimit

    heightDiffofPelvis = (knees_Y - pelvis_Y) / thigh * 100

    return (fall, heightDiffofPelvis)










