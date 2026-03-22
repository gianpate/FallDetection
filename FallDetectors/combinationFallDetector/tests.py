from utils.paths import get_flagged_samples
from utils.parsers.JSONparsers import basicParser
from itertools import combinations
import recognizers as rec
import os
import matplotlib.pyplot as plt


N_RECOGNIZERS = 6
FALLS = 29
NO_FALLS = 31



def get_recognizer_results(joints:dict): 
    return {
        "D": rec.directionRecognizer(joints)[0],
        "P": rec.pelvisDownRecognizer(joints)[0],
        "H": rec.handsDownRecognizer(joints)[0],
        "S": rec.spanRecognizer(joints)[0],      
        "T": rec.trunkAngleRecognizer(joints)[0],
        "K": rec.kneesDownRecognizer(joints)[0],
    }



def initiate_table():
    """
    returns an accumulative table of {TP, TN} counts
               threshold
            1      2      3      4   .... 
    c  1  { , }  { , }    ...   ... 
    o  2  { , }  { , }    ...   ...
    m  3    ...   ...     ...   ...
    b  .    ...   ...     ...   ...
       .    ...   ...     ...   ...
       .
    """
    table = [[{"TP": 0, "TN": 0} for t in range(0, 20)] for n in range(0, 6)]
    return table 


def get_recognizer_combinations(n):
    r = ["D", "P", "H", "S", "T", "K"]
    return list(combinations(r, n))



def evaluate_combinations(combinations, predicates):
    """
    Return a list of booleans: one per combination, where each element is
    the AND of the predicate values for the keys in that combination.
    """
    return [all(predicates[key] for key in combo) for combo in combinations]



def testConfigurations(table, samples):
    global N_RECOGNIZERS
    
    for sample, expected in samples:
        joints = basicParser(sample)  
        predicates = get_recognizer_results(joints)  

        for n in range(1, N_RECOGNIZERS + 1):
            combin = get_recognizer_combinations(n)
            thresholds = len(combin)
            conjunctions = evaluate_combinations(combin, predicates)
            score = sum(conjunctions)   # number of trues
            # for conjunc n   => index = n-1 
            # for threshold t => index = t-1 leftshift already in the range()
            if expected == True:
                for t in range(0, score):   # if true all thresholds <= score will detect
                    table[n-1][t]["TP"] += 1
            else: 
                for t in range(score, thresholds): # if false all thresholds > score will detect
                    table[n-1][t]["TN"] += 1




def plot_config(table:list, n:int, stats:list, plotnames:list):
    """
    For a given combination size n (1..6), extract the corresponding row from table,
    compute TP%, TN%, and Success% for thresholds 1..20, plot them and 
    append (n, best_TP_thresh, best_TN_thresh, best_success_thresh) to stats.
    append plot png name in the plotnames list
    """
    
    global FALLS 
    global NO_FALLS 
    TOTAL = FALLS + NO_FALLS

    row = table[n-1]   # list of 20 dicts with keys "TP", "TN"
    
    thresholds = list(range(1, 21))  # x-axis values: 1, 2, ..., 20
    
    tp_pct = []
    tn_pct = []
    success_pct = []
    
    # For storing max 
    best_TP = -1
    best_TN = -1
    best_success = -1
    best_TP_thresh = None
    best_TN_thresh = None
    best_success_thresh = None
    
    for t, cell in enumerate(row, start=1):
        tp = cell["TP"]
        tn = cell["TN"]
        success = tp + tn
        
        tp_pct.append((tp / FALLS) * 100)
        tn_pct.append((tn / NO_FALLS) * 100)
        success_pct.append((success / TOTAL) * 100)
        
        # Track max values
        if tp > best_TP:
            best_TP = tp
            best_TP_thresh = t
        if tn > best_TN:
            best_TN = tn
            best_TN_thresh = t
        if success > best_success:
            best_success = success
            best_success_thresh = t
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(thresholds, tp_pct, 'b-o', label='TP%')
    plt.plot(thresholds, tn_pct, 'g-s', label='TN%')
    plt.plot(thresholds, success_pct, 'r-^', label='Success%')
    plt.xlabel('Threshold')
    plt.ylabel('Percentage (%)')
    plt.title(f'Performance for combination size n = {n}')
    plt.legend()
    plt.grid(True)
    
    # store plot
    os.makedirs('./FallDetectors/combinationFallDetector/results', exist_ok=True)
    filename = f'./FallDetectors/combinationFallDetector/results/config_{n}.png'
    plt.savefig(filename, dpi=150)
    plt.close()  

    plotnames.append(filename)
    
    # Append the best thresholds to stats list
    stats.append((n, best_TP_thresh, best_TN_thresh, best_success_thresh))




def generate_report(table, stats, plotnames, output_dir='./FallDetectors/combinationFallDetector/results'):
    """
    Create a markdown report in ./results/report.md summarizing the results.
    stats: list of (n, best_TP_thresh, best_TN_thresh, best_success_thresh)
    plotnames: list of filenames (e.g., 'config_1.png', ...)
    table: the 2D table of TP/TN counts (list of rows, each row list of dicts)
    """
    # Global constants (assume they are defined at module level)
    global FALLS, NO_FALLS
    TOTAL = FALLS + NO_FALLS

    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "report.md")

    with open(report_path, "w") as f:
        f.write("# Configuration Performance Report\n\n")
        f.write("This report summarizes the best thresholds for each combination size (n) and highlights the overall best configuration.\n\n")

        # For each n, extract the best thresholds from stats
        # stats is in order of n, but we'll loop explicitly over n=1..6
        # We'll map n to its stats entry
        stats_dict = {entry[0]: entry for entry in stats}
        plot_dict = plot_dict = {int(os.path.basename(name).split('_')[1].split('.')[0]): os.path.basename(name) for name in plotnames}
        for n in range(1, 7):
            if n not in stats_dict:
                continue   # should not happen, but safety
            n_stats = stats_dict[n]
            best_TP_thresh = n_stats[1]
            best_TN_thresh = n_stats[2]
            best_success_thresh = n_stats[3]

            # Get counts from the table
            row = table[n-1]   # list of 20 dicts
            # TP at best_TP_thresh (threshold = best_TP_thresh)
            tp = row[best_TP_thresh - 1]["TP"] if best_TP_thresh is not None else 0
            tn = row[best_TN_thresh - 1]["TN"] if best_TN_thresh is not None else 0
            # For success threshold, we use its TP and TN
            tp_s = row[best_success_thresh - 1]["TP"] if best_success_thresh is not None else 0
            tn_s = row[best_success_thresh - 1]["TN"] if best_success_thresh is not None else 0

            # Percentages
            tp_pct = (tp / FALLS) * 100 if FALLS > 0 else 0
            tn_pct = (tn / NO_FALLS) * 100 if NO_FALLS > 0 else 0
            success_pct = (tp_s + tn_s) / TOTAL * 100 if TOTAL > 0 else 0

            # Write section for this n
            f.write(f"## Configuration n = {n}\n\n")
            # Show plot as thumbnail
            plot_filename = plot_dict.get(n, f"config_{n}.png")
            f.write(f'<img src="{plot_filename}" width="700" alt="Performance for n={n}"/>\n\n')
            f.write("| Metric | Best Threshold | Value | Percentage |\n")
            f.write("|--------|----------------|-------|------------|\n")
            f.write(f"| True Positives (TP) | {best_TP_thresh} | {tp} | {tp_pct:.1f}% |\n")
            f.write(f"| True Negatives (TN) | {best_TN_thresh} | {tn} | {tn_pct:.1f}% |\n")
            f.write(f"| Success (TP+TN) | {best_success_thresh} | {tp_s + tn_s} | {success_pct:.1f}% |\n\n")

        # Find overall best configuration (by success percentage)
        # Find overall best configuration(s) by success percentage
        max_success_pct = -1.0
        best_configs = []   # list of (n, thresh, tp, tn, pct)

        for n in range(1, 7):
            if n not in stats_dict:
                continue
            n_stats = stats_dict[n]
            best_success_thresh = n_stats[3]
            if best_success_thresh is None:
                continue
            row = table[n-1]
            tp_s = row[best_success_thresh - 1]["TP"]
            tn_s = row[best_success_thresh - 1]["TN"]
            pct = (tp_s + tn_s) / TOTAL * 100 if TOTAL > 0 else 0

            if pct > max_success_pct:
                max_success_pct = pct
                best_configs = [(n, best_success_thresh, tp_s, tn_s, pct)]
            elif pct == max_success_pct:
                best_configs.append((n, best_success_thresh, tp_s, tn_s, pct))

        f.write("## Overall Best Configuration(s)\n\n")
        if best_configs:
            # Table header
            f.write("| n | Threshold | TP (%) | TP (count) | TN (%) | TN (count) | Success (%) |\n")
            f.write("|---|-----------|--------|------------|--------|------------|-------------|\n")
            for n, thresh, tp_s, tn_s, pct in best_configs:
                tp_pct = (tp_s / FALLS) * 100 if FALLS > 0 else 0
                tn_pct = (tn_s / NO_FALLS) * 100 if NO_FALLS > 0 else 0
                f.write(f"| {n} | {thresh} | {tp_pct:.1f}% | {tp_s}/{FALLS} | {tn_pct:.1f}% | {tn_s}/{NO_FALLS} | {pct:.1f}% |\n")
            f.write("\n")
        else:
            f.write("No configuration found.\n")

    print(f"Report saved to {report_path}")





def run():
    table = initiate_table()
    samples = get_flagged_samples()
    stats = []
    plotnames = []

    testConfigurations(table, samples)

    for n in range(1, N_RECOGNIZERS+1):
        plot_config(table, n, stats, plotnames)

    generate_report(table, stats, plotnames)


       



    
    

