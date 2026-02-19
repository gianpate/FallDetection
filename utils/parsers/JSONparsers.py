import json
import os
from utils.paths import skeletonJson_path


def filter_joints(data, filter):
    """
    Returns a new dictionary containing only the key-value pairs
    where the key is in keep_keys.
    """
    return {key: data[key] for key in filter if key in data}



#  BASIC parser keeps basic joints

BASIC_points = [
    "pelvis", "spine1", "spine2", "spine3", "neck",
    "left_collar", "right_collar", "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow", "left_wrist", "right_wrist",
    "left_hand_thumb4", "right_hand_thumb4",
    "left_hip", "right_hip", "left_knee", "right_knee",
    "left_ankle", "right_ankle", "left_foot", "right_foot",
    "head", "head_nose"
]

def basicParser(inputDirectory, samplesDir="samples"):
    inputDirectory = os.path.join(samplesDir, inputDirectory)
    jsonFile = skeletonJson_path(inputDirectory)
    with open(jsonFile, 'r') as f:
        data = json.load(f)

    filtered = filter_joints(data, BASIC_points)
    return filtered

    

