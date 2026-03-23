
import os

def skeletonJson_path(directory):
    """
    returns the path of the skeleton.json inside the the sample diretory
    """
    skeleton_files = [f for f in os.listdir(directory) if f.startswith("skeleton") and f.endswith(".json")]
    
    if not skeleton_files:
        raise FileNotFoundError("No skeleton JSON file found in the input directory.")
    
    path = os.path.join(directory, skeleton_files[0])  # assume 1 skeleton
    return path



def generate_sample_names(start, end, step=1, prefix='sample_', digits=5):
    """
    Returns: list of strings: e.g., ['sample_00001', 'sample_00002', ...]
    """
    return [f"{prefix}{i:0{digits}d}" for i in range(start, end + 1, step)]



def get_allSamples(fall_count, nofall_count):
    """
    returns (fall sample paths, no fall sample paths)
    """
    fall_dir = "Fall"
    nofall_dir = "NoFall"

    fallSamples = [os.path.join(fall_dir, path) for path in generate_sample_names(1, fall_count)] 
    noFallSamples = [os.path.join(nofall_dir, path) for path in generate_sample_names(1, nofall_count)]
    return (fallSamples, noFallSamples)



def get_flagged_samples():
    """
    returns list pf tuples (samplename, flag)
    """
    FALLS = 29
    NO_FALLS = 31

    fallSamples, noFallSamples = get_allSamples(FALLS, NO_FALLS)
    samples = []
    for sample in fallSamples:
        samples.append((sample, True))   # fall expected
    for sample in noFallSamples:
        samples.append((sample, False))  # no fall expected

    return samples