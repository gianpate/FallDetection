import numpy as np
from utils.vectors import distance

def get_PoseDirection(joints:dict):
    head = np.array(joints["head"])
    rightShoulder = np.array(joints["right_shoulder"])
    leftShoulder = np.array(joints["left_shoulder"])

    head_left =  leftShoulder - head
    head_right = rightShoulder - head

    direction = np.cross(head_left, head_right)

    return direction



def get_legLength(joints:dict):
    leftAnkle = np.array(joints["left_ankle"])
    leftKnee = np.array(joints["left_knee"])
    leftHip = np.array(joints["left_hip"])
    leftLeg = distance(leftAnkle, leftKnee) + distance(leftKnee, leftHip)

    rightAnkle = np.array(joints["right_ankle"])
    rightKnee = np.array(joints["right_knee"])
    rightHip = np.array(joints["right_hip"])
    rightLeg = distance(rightAnkle, rightKnee) + distance(rightKnee, rightHip)

    return (leftLeg + rightLeg) / 2.0



def get_shinLength(joints:dict):
    leftAnkle = np.array(joints["left_ankle"])
    leftKnee = np.array(joints["left_knee"])
    leftShin = distance(leftAnkle, leftKnee)

    rightAnkle = np.array(joints["right_ankle"])
    rightKnee = np.array(joints["right_knee"])
    rightShin = distance(rightAnkle, rightKnee)

    return (leftShin + rightShin) / 2.0



def get_feetLevel(joints):
    leftAnkle = np.array(joints["left_ankle"])
    rightAnkle = np.array(joints["right_ankle"])
    
    # feetLevel = (leftAnkle + rightAnkle) / 2
    feetLevel = leftAnkle if leftAnkle[1] > rightAnkle[1] else rightAnkle

    return feetLevel


def get_handsLevel(joints:dict):
    rightHand = np.array(joints["right_wrist"])
    leftHand = np.array(joints["left_wrist"])

    handsLevel = leftHand if leftHand[1] > rightHand[1] else rightHand

    return handsLevel


def get_headToPelvisHeight(joints:dict):
    head = np.array(joints["head"])
    neck = np.array(joints["neck"])
    spine3 = np.array(joints["spine3"])
    spine2 = np.array(joints["spine2"])
    spine1 = np.array(joints["spine1"])
    pelvis = np.array(joints["pelvis"])

    trunk = (
        distance(head, neck) + 
        distance(neck, spine3) +
        distance(spine3, spine2) + 
        distance(spine2, spine1) +
        distance(spine1, pelvis)
    )

    return trunk


def get_personHeight(joints: dict):
    return get_headToPelvisHeight(joints) + get_legLength(joints)
