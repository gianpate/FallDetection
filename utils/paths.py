
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