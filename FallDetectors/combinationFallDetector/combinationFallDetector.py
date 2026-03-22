import recognizers as rec

# | n | t |  TP   |  TN   | total |
# | 1 | 5 | 23/29 | 26/31 | 81.7% |
# | 2 | 7 | 23/29 | 26/31 | 81.7% |
# | 3 | 5 | 23/29 | 26/31 | 81.7% |
# | 4 | 2 | 23/29 | 26/31 | 81.7% |
# | 5 | 1 | 23/29 | 26/31 | 81.7% |
# => (n, t) = (1, 5) the simplest with same results


def combinationFallDetector(joints:dict) -> bool:
    """
    returns true if threshold recognizers are true 
    threshold = 5
    """
    THRESHOLD = 5
    
    recognizers = rec.get_recognizers()

    count = 0
    for r in recognizers:
        count += r(joints)[0]
        if count == THRESHOLD:
            return True
    return False
