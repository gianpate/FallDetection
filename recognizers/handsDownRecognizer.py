import numpy as np
from poseProperties import (
    get_feetLevel, 
    get_shinLength, 
    get_handsLevel,
    get_personHeight
)

def handsDownRecognizer(joints:dict) -> tuple:
    """
    returns true if hands lower than the height of the knee t[0]
    how far up and down from head (if upright) t[1]:
        - 100%    down
        - 0%      up
        - >100%   hands below feet
        - <0%     hands above head
    """
    feetLevel = get_feetLevel(joints)
    handsLevel = get_handsLevel(joints)

    feet_Y = feetLevel[1]
    hands_Y = handsLevel[1]

    shin = get_shinLength(joints)
    #  -y => up so we subtract
    handsHeightLimit = feet_Y - shin 

    fall = hands_Y > handsHeightLimit

    personHeight = get_personHeight(joints)
    heightDifFromHands = 100 + (hands_Y - feet_Y) / personHeight * 100

    return (fall, heightDifFromHands)


