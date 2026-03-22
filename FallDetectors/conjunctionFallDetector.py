import recognizers as rec


def conjunctionFallDetector(joints:dict) -> bool:
    """
    if horizontal span negative => definately NoFall
    if positive => span && pelvisDown => pelvisDown
        if pelvis down => Fall else NoFall
    """
    if rec.spanRecognizer(joints)[0]:
        return rec.pelvisDownRecognizer(joints)[0]
    else:
        return False

