import FallDetectors as fd
from utils.paths import get_allSamples
from utils.parsers.JSONparsers import basicParser

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"


def runFallDetector(detector, samples):
    fallSamples, noFallSamples = samples

    for sample in fallSamples:
        joints = basicParser(sample)
        result = detector(joints)
        status = f"{GREEN}pass{RESET}" if result else f"{RED}fail{RESET}"
        print(f"{sample} : ", status)

    # print()  blank line

    for sample in noFallSamples:
        joints = basicParser(sample)
        result = detector(joints)
        status = f"{GREEN}pass{RESET}" if not result else f"{RED}fail{RESET}"
        print(f"{sample} : ", status)





if __name__ == "__main__":
    
    samples = get_allSamples(29, 31)

    print("conjunction detector \n")
    runFallDetector(fd.conjunctionFallDetector, samples)
    print("\n weighted score detector")
    runFallDetector(fd.weightedFallDetector, samples)
