import recognizers as rec


def weightedFallDetector(joints:dict) -> bool:
    """
    weighted fall decision using all recognizers
    score = Σ(weight * recognizer_result_flag)
    returns true if score >= threshold
    """
    recognizers = [
        (rec.directionRecognizer, 1),
        (rec.pelvisDownRecognizer, 3),
        (rec.handsDownRecognizer, 1),
        (rec.spanRecognizer, 3),       
        (rec.trunkAngleRecognizer, 1),
        (rec.kneesDownRecognizer, 1),
    ]

    weighted_sum = sum(
        weight * int(func(joints)[0])
        for func, weight in recognizers
    )

    THRESHOLD = 7

    return weighted_sum >= THRESHOLD    

    