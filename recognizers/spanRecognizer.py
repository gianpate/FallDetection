import numpy as np
from utils.vectors import distance

def spanRecognizer(joints:dict) -> tuple:
    
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

    fallSpan = horizontalSpan > delta_Y

    percentageOfDeltaY = horizontalSpan / delta_Y * 100

    return (fallSpan, percentageOfDeltaY)







    

