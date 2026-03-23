import csv
import os
from utils.parsers.JSONparsers import basicParser

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
    joints = basicParser(sample_name)
    row = [sample_name]
    for rec in recognizers:
        _, value = rec(joints)
        row.append(value)
    row.append(1 if expected else 0)   # expected as 0/1
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