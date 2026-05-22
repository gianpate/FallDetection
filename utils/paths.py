
import os
import re
import csv

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
    returns list of tuples (samplename, flag)
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



def get_video_paths_URFD(dataset_base):
    """
    Returns a sorted list of paths to video directories
    Each directory name should match 'adl-XX' or 'fall-XX'
    """
    videos = []
    for entry in os.listdir(dataset_base):
        full_path = os.path.join(dataset_base, entry)
        if os.path.isdir(full_path) and re.match(r'(adl|fall)-\d+', entry):
            videos.append(full_path)
    return sorted(videos)


def get_labeled_dataset_URFD(base_dir):
    """
    Returns a dictionary: {video_name: [(frame_path, label), ...], ...}
    """
    # get the list of video directories (to know which videos exist)
    video_paths = get_video_paths_URFD(base_dir)
    result = {}

    for csv_name in ['adls.csv', 'falls.csv']:
        csv_path = os.path.join(base_dir, csv_name)
        
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                video_name = row[0].strip()
                frame_num = int(row[1])
                label = int(row[2])

                # Construct the expected frame file path
                frame_file = f"frame_{frame_num:03d}.json"
                frame_path = os.path.join(base_dir, video_name, frame_file)

                # Only add if the file actually exists (this automatically skips even frame numbers)
                if os.path.exists(frame_path):
                    if video_name not in result:
                        result[video_name] = []
                    result[video_name].append((frame_path, label))

    return result