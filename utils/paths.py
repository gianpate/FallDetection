
import os

def skeletonJson_path(directory):
    skeleton_files = [f for f in os.listdir(directory) if f.startswith("skeleton") and f.endswith(".json")]
    
    if not skeleton_files:
        raise FileNotFoundError("No skeleton JSON file found in the input directory.")
    
    path = os.path.join(directory, skeleton_files[0])  # assume 1 skeleton
    return path