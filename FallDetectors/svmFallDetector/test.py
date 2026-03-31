import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.svm import SVC 
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

#test scaling
# , c, gamma, kernel, and degree for polynom

def fetch_samples_and_lables(dataCSV):
    df = pd.read_csv(dataCSV)

    x = df.drop(columns=['sample_name', 'expected'])  # recognizer columns
    y = df['expected']                                # target labels

    return x, y

    

def teststardardization(x, y, skf):

    svm = SVC()
    standardizedSvm = make_pipeline(StandardScaler(), SVC())

    scores_noStandardization = cross_val_score(svm, x, y, cv=skf)
    scores_Standardization = cross_val_score(standardizedSvm, x, y, cv=skf)

    return scores_noStandardization, scores_Standardization


def plot_comparison_simple(scores_noStandardization, scores_Standardization, save_path=None):
    
    folds = range(1, len(scores_noStandardization) + 1)
    bar_width = 0.35
    
    plt.figure(figsize=(10, 6))
    
    plt.bar([f - bar_width/2 for f in folds], scores_noStandardization, 
            bar_width, label='Without Scaling', color='red', alpha=0.7)
    plt.bar([f + bar_width/2 for f in folds], scores_Standardization, 
            bar_width, label='With Scaling', color='blue', alpha=0.7)
    
    plt.axhline(y=np.mean(scores_noStandardization), color='red', linestyle='--', 
                label=f'Mean No Scaling: {np.mean(scores_noStandardization):.3f}')
    plt.axhline(y=np.mean(scores_Standardization), color='blue', linestyle='--', 
                label=f'Mean Scaling: {np.mean(scores_Standardization):.3f}')
    
    plt.xlabel('Fold')
    plt.ylabel('Accuracy')
    plt.title('SVM: Scaling vs No Scaling')
    plt.xticks(folds)
    plt.ylim(0, 1)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    if save_path:
        plt.savefig(os.path.join(save_path, "standardVsNostandard.jpg"), dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()


def test_standardization_on_kernels(x, y, skf):
    """
    Test all kernels with and without standardization.
    """
    
    kernels = ['linear', 'rbf', 'poly', 'sigmoid']
    results = {}
    
    for kernel in kernels:
        # Without standardization
        svm = SVC(kernel=kernel)
        scores_no = cross_val_score(svm, x, y, cv=skf)
        
        # With standardization
        svm_std = make_pipeline(StandardScaler(), SVC(kernel=kernel))
        scores_std = cross_val_score(svm_std, x, y, cv=skf)
        
        results[kernel] = {
            'no_std_mean': np.mean(scores_no),
            'no_std_std': np.std(scores_no),
            'std_mean': np.mean(scores_std),
            'std_std': np.std(scores_std),
        }
    
    return results


def plot_kernel_std_comparison(results, save_path=None):
    kernels = list(results.keys())
    no_std_means = [results[k]['no_std_mean'] for k in kernels]
    std_means = [results[k]['std_mean'] for k in kernels]
    no_std_err = [results[k]['no_std_std'] for k in kernels]
    std_err = [results[k]['std_std'] for k in kernels]
    
    x = np.arange(len(kernels))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bars with error bars
    bars1 = ax.bar(x - width/2, no_std_means, width, yerr=no_std_err, 
                   label='Without Standardization', color='red', alpha=0.7, 
                   capsize=5, error_kw={'linewidth': 2})
    bars2 = ax.bar(x + width/2, std_means, width, yerr=std_err,
                   label='With Standardization', color='blue', alpha=0.7,
                   capsize=5, error_kw={'linewidth': 2})
    
    # Connecting lines
    ax.plot(x - width/2, no_std_means, linestyle='--' , color='red', linewidth=2, markersize=8)
    ax.plot(x + width/2, std_means, linestyle='--', color='blue', linewidth=2, markersize=8)
    
    ax.set_xlabel('Kernel')
    ax.set_ylabel('Mean Accuracy')
    ax.set_title('SVM Performance: Standardization Effect Across Kernels')
    ax.set_xticks(x)
    ax.set_xticklabels(kernels)
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    if save_path:
        plt.savefig(os.path.join(save_path, "StandardizationOnKernels.jpg"), dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()



def test_c(x, y, skf, kernels, c_values):
    """
    Tune C parameter for each kernel (with standardization).
    """
    results = {}
    
    for kernel in kernels:
        results[kernel] = {}
        for c in c_values:
            # create pipeline with standardization
            pipeline = make_pipeline(StandardScaler(), SVC(kernel=kernel, C=c))
            scores = cross_val_score(pipeline, x, y, cv=skf)
            results[kernel][c] = np.mean(scores)
    
    return results


def test_gamma(x, y, skf, kernels, gamma_values):
    """
    Tune gamma parameter for each kernel (with standardization).
    """
    results = {}
    
    for kernel in kernels:
        results[kernel] = {}
        for gamma in gamma_values:
            # create pipeline with standardization
            pipeline = make_pipeline(StandardScaler(), SVC(kernel=kernel, gamma=gamma))
            scores = cross_val_score(pipeline, x, y, cv=skf)
            results[kernel][gamma] = np.mean(scores)
    
    return results



def plot_tuning_results(results, param_name, save_path=None):
    """
    Plot tuning results for all kernels.
    
    results: nested dict {kernel: {param_value: mean_score}}
    param_name: 'C' or 'gamma'
    save_path: optional path to save plot
    """
    
    plt.figure(figsize=(10, 6))
    
    # Get all param values 
    first_kernel = list(results.keys())[0]
    param_values = list(results[first_kernel].keys())
    
    # Plot each kernel
    for kernel, scores_dict in results.items():
        # Get scores to a list
        scores = [scores_dict[val] for val in param_values]
        
        # Convert to strings (handles both numbers and strings)
        x_labels = [str(val) for val in param_values]
        x_positions = range(len(param_values))
        
        plt.plot(x_positions, scores, 'o-', label=kernel.upper(), linewidth=2, markersize=8)
    
    plt.xticks(x_positions, x_labels)
    plt.xlabel(param_name)
    plt.ylabel('Mean Cross-Validation Accuracy')
    plt.title(f'Tuning {param_name}')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.ylim(0, 1)
    
    if save_path:
        plt.savefig(os.path.join(save_path, f"test_{param_name}.jpg"), dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    else:
        plt.show()
    
    plt.close()



def runTest(dataCSV, save_path=None):
    x, y = fetch_samples_and_lables(dataCSV)
    
    #cross validation spliter
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # scores = teststardardization(x, y, skf)
    # plot_comparison_simple(scores[0], scores[1], save_path)

    # r = test_standardization_on_kernels(x, y, skf)
    # plot_kernel_std_comparison(r, save_path)

    kernels = ['linear', 'rbf', 'poly', 'sigmoid']
    c_values = [0.1, 1, 10, 100]
    r = test_c(x, y, skf, kernels, c_values)
    plot_tuning_results(r, "C", save_path)

    
    kernels = ['rbf', 'poly', 'sigmoid']
    gamma_values = ['scale', 'auto', 0.1, 1, 10]
    r = test_gamma(x, y, skf, kernels, gamma_values)
    plot_tuning_results(r, "gamma", save_path)