import numpy as np
from utils.vectors import distance
from poseProperties import (
    get_legLength, 
    get_shinLength, 
    get_feetLevel
)


def pelvisDownRecognizer(joints:dict) -> tuple:
    """
    returns true if pelvis lower than the height of the knee t[0]
    how far up and down from straight up t[1]:
        - 100%    down
        - 0%      upright
        - >100%   pelvis below feet 
    """
    pelvis = np.array(joints["pelvis"])

    shin = get_shinLength(joints)
    leg = get_legLength(joints)

    feetLevel = get_feetLevel(joints)

    feet_Y = feetLevel[1]
    pelvis_Y = pelvis[1]

    #  -y => up so we subtract
    pelvisHeightLimit = feet_Y - shin 
    
    fall = pelvis_Y > pelvisHeightLimit

    raw_percentageHeight =  100 + (pelvis_Y - feet_Y) / leg * 100
    heightDifFromPelvis = max(0, raw_percentageHeight)

    return (fall, heightDifFromPelvis)
