import csv
import os
from utils.parsers.JSONparsers import basicParser, directBasicParser

def init_csv(recognizers, filepath='data/recognizer_results.csv'):
    """
    Create (or overwrite) a CSV file with header:
    sample_name, <rec1_name>, <rec2_name>, ..., expected
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        header = ['sample_name'] + [rec.__name__ for rec in recognizers] + ['expected']
        writer.writerow(header)



def append_sample(sample_tuple, recognizers, filepath='data/recognizer_results.csv'):
    """
    For a single sample (sample_name, expected_flag), compute the float output of each recognizer
    and append a row to the CSV: sample_name, rec1_value, rec2_value, ..., expected
    """
    sample_name, expected = sample_tuple
    if sample_name.endswith('.json'):
        joints = directBasicParser(sample_name)
    else: 
        joints = basicParser(sample_name)
    row = [sample_name]
    for rec in recognizers:
        _, value = rec(joints)
        row.append(value)
    row.append(expected)
    with open(filepath, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)


def recognizer_results_to_csv(samples, recognizers, filepath='data/recognizer_results.csv'):
    """
    create the CSV file and fill it with all samples.
    """
    init_csv(recognizers, filepath)
    for sample in samples:
        append_sample(sample, recognizers, filepath)

### ======================= URDF =========================== ###

def remove_label_zero(samples):
    """
    Returns a new list containing only tuples where label != 0.
    """
    for video_name, frame_list in samples.items():
        samples[video_name] = [(path, label) for path, label in frame_list if label != 0]


def recognizers_URFD_to_csv(samples, recognizers,  output_dir="./data/URFD"):
    """
    creates the csvs for each URFD video from the recognizers and the flags
    """
    os.makedirs(output_dir, exist_ok=True)
    remove_label_zero(samples)
    for video_name, frame_list in samples.items():
        filepath = os.path.join(output_dir, f"{video_name}.csv")
        recognizer_results_to_csv(frame_list, recognizers, filepath)


### ======================================================== ###