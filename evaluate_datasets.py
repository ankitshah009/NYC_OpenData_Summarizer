import pandas as pd
from io import StringIO
import json
import os

#This function takes a file path of a JSON file as input, reads the JSON content, and converts it to a pandas DataFrame.
def load_json_to_dataframe(file_path):
    """
    Loads JSON content from a file and returns it as a pandas DataFrame.
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    # Convert to DataFrame
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        raise ValueError("Unsupported JSON structure.")
        
    return df

# Computes a completeness score for the dataset, which is based on the proportion of non-missing values.
def compute_completeness_score(df):
    """
    Computes the completeness score of the dataset based on missing values.
    Score = (Total number of values - Number of missing values) / Total number of values
    """
    total_values = df.size
    missing_values = df.isnull().sum().sum()
    completeness_score = (total_values - missing_values) / total_values
    return completeness_score


def compute_variability_score(df):
    """
    Computes the variability score for each column in the dataset.
    This function returns a dictionary with column names as keys and variability scores as values.
    Variability Score = Number of unique values / Total number of values in the column
    """
    variability_scores = {}
    for column in df.columns:
        if all(isinstance(item, (int, float, str, bool, type(None))) for item in df[column]):
            num_unique_values = df[column].nunique()
            total_values = len(df[column])
            variability_scores[column] = num_unique_values / total_values
        else:
            print(f"Warning: Skipping column '{column}' as it contains unhashable types (e.g., dictionaries).")
    return variability_scores

def evaluate_transparency_of_dataset(file_path):
    """
    Evaluates the transparency of a dataset given its file path.
    """

    df = load_json_to_dataframe(file_path)

    # Calculate metrics
    completeness = compute_completeness_score(df)
    variability = compute_variability_score(df)

    # Print results
    print(f"Completeness Score: {completeness:.2f}")
    print("Variability Scores per Column:")
    for column, score in variability.items():
        print(f"{column}: {score:.2f}")

    return completeness, variability



def compute_representation_score(df, column):
    """
    Computes the representation score for a categorical column.
    This function returns the distribution of values in the column.
    """
    if all(isinstance(item, (int, float, str, bool, type(None))) for item in df[column]):
        total_values = len(df[column])
        representation_scores = df[column].value_counts() / total_values
        return representation_scores
    else:
        print(f"Warning: Skipping column '{column}' as it contains unhashable types (e.g., dictionaries).")
        return None

def evaluate_bias_of_dataset(file_path, categorical_columns):
    """
    Evaluates potential bias in a dataset based on representation in specified categorical columns.
    
    Args:
    - file_path: Path to the dataset.
    - categorical_columns: List of columns to check for representation bias.
    
    Returns:
    - Dictionary of representation scores for each specified column.
    """
    df = load_json_to_dataframe(file_path)
    #df = pd.read_csv(file_path)
    
    bias_scores = {}
    
    for column in categorical_columns:
        if column in df.columns:
            representation = compute_representation_score(df, column)
            bias_scores[column] = representation
        else:
            print(f"Warning: {column} not found in the dataset.")
    
    # Print results
    for column, scores in bias_scores.items():
        print(f"\nRepresentation in {column}:")
        for category, score in scores.items():
            print(f"{category}: {score:.2f}")

    return bias_scores


def compute_balance_score(df, protected_column, outcome_column):
    """
    Computes the balance score for a protected attribute in relation to an outcome.
    This function returns the ratio of positive outcomes for each group in the protected column.
    """
    groups = df[protected_column].unique()
    balance_scores = {}
    
    for group in groups:
        subset = df[df[protected_column] == group]
        positive_outcomes = sum(subset[outcome_column] == 1)
        total_instances = len(subset)
        balance_scores[group] = positive_outcomes / total_instances if total_instances != 0 else 0
    
    return balance_scores

def evaluate_fairness_of_dataset(file_path, protected_columns, outcome_column):
    """
    Evaluates potential fairness issues in a dataset based on balance of positive outcomes in specified protected columns.
    
    Args:
    - file_path: Path to the dataset.
    - protected_columns: List of columns representing protected attributes.
    - outcome_column: Column representing the outcome (1 for positive outcome, 0 for negative).
    
    Returns:
    - Dictionary of balance scores for each specified protected column.
    """
    #df = pd.read_csv(file_path)
    df = load_json_to_dataframe(file_path)
    
    fairness_scores = {}
    
    for column in protected_columns:
        if column in df.columns:
            balance = compute_balance_score(df, column, outcome_column)
            fairness_scores[column] = balance
        else:
            print(f"Warning: {column} not found in the dataset.")
    
    # Print results
    for column, scores in fairness_scores.items():
        print(f"\nPositive Outcome Balance in {column}:")
        for category, score in scores.items():
            print(f"{category}: {score:.2f}")

    return fairness_scores



'''
# Example usage:
file_path = 'path_to_your_dataset.json'
protected_columns_to_check = ['gender', 'race']  # Modify this list based on your dataset's columns
outcome_column_name = 'loan_approval'  # Modify this based on your dataset's outcome column
evaluate_fairness_of_dataset(file_path, protected_columns_to_check, outcome_column_name)

# Example usage:
file_path = 'path_to_your_dataset.json'
categorical_columns_to_check = ['gender', 'race', 'ethnicity']  # Modify this list based on your dataset's columns
evaluate_bias_of_dataset(file_path, categorical_columns_to_check)

# Example usage:
file_path = 'path_to_your_dataset.json'
evaluate_transparency_of_dataset(file_path)
'''

import pandas as pd
import json
import os

def load_json_to_dataframe(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    if isinstance(data, list):
        df = pd.DataFrame(data)
    elif isinstance(data, dict):
        df = pd.DataFrame([data])
    else:
        raise ValueError("Unsupported JSON structure.")
        
    return df

# ... [Keep the existing functions unchanged] ...

def rank_files_based_on_scores(directory_path):
    """
    Ranks files in a directory based on computed scores from each function.
    """
    scores = {}
    
    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        
        # Ensure we are only processing JSON files
        if not file_name.endswith('.json'):
            continue
        
        print(f"Evaluating file: {file_name}")
        
        # Compute scores for each file
        completeness, variability = evaluate_transparency_of_dataset(file_path)
        #bias_scores = evaluate_bias_of_dataset(file_path, categorical_columns_to_check)
        #fairness_scores = evaluate_fairness_of_dataset(file_path, protected_columns_to_check, outcome_column_name)

        
        # Aggregate scores for ranking later
        scores[file_name] = {
            'completeness': completeness,
            'variability_avg': sum(variability.values()) / len(variability) if variability else 0
            #'bias_scores' : bias_scores
            #'fairness_scores' : fairness_scores
            # Add any other scores that you want to rank on
        }
    
    # Rank files based on completeness and then variability
    sorted_files = sorted(scores.keys(), key=lambda x: (scores[x]['completeness'], scores[x]['variability_avg']), reverse=True)
    output = []
    print("\nRanked Files:")
    for rank, file_name in enumerate(sorted_files, 1):
        print(f"{rank}. {file_name} - Completeness: {scores[file_name]['completeness']:.2f}, Variability Avg: {scores[file_name]['variability_avg']:.2f}")
        output.append(f"{rank}. {file_name} - Completeness: {scores[file_name]['completeness']:.2f}, Variability Avg: {scores[file_name]['variability_avg']:.2f}")
    return output

# Define directory path and required columns
# directory_path = './path_to_your_folder'
# protected_columns_to_check = ['gender', 'race']
# outcome_column_name = 'loan_approval'
# categorical_columns_to_check = ['gender', 'race', 'ethnicity']

# ranked_files = rank_files_based_on_scores(directory_path)
