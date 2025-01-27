import pandas as pd
import numpy as np
import itertools
from sklearn.metrics import mutual_info_score
from sklearn.preprocessing import LabelEncoder
import os
import glob
from tqdm import tqdm


def compute_max_mutual_information(input_directory, output_csv):
    """
    Processes all CSV files in the input_directory, computes mutual information for all
    pairs of the first 50 variables with the class label, and saves the maximum mutual
    information value for each file into output_csv.

    Parameters:
    - input_directory (str): Path to the directory containing input CSV files.
    - output_csv (str): Path to the output CSV file to save results.
    """

    # Pattern to match CSV files. Adjust the pattern if necessary.
    csv_pattern = os.path.join(input_directory, "2_EDM-1_*.csv")
    file_list = glob.glob(csv_pattern)

    if not file_list:
        print(f"No CSV files found in the directory: {input_directory}")
        return

    print(f"Found {len(file_list)} CSV files to process.")

    # Prepare a list to store the results
    results = []

    # Iterate over each file with a progress bar
    for file_path in tqdm(file_list, desc="Processing files"):
        try:
            # Read the CSV file
            # Adjust header, separator, and encoding as needed
            try:
                df = pd.read_csv(file_path, sep=",", header=0, encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, sep=",", header=0, encoding='gbk')

            # Verify the data
            num_rows, num_cols = df.shape
            if num_cols < 51:
                print(f"Skipping file {os.path.basename(file_path)}: Not enough columns ({num_cols})")
                continue  # Skip files that do not have at least 50 variables + 1 class column

            # Select the first 50 variable columns and the last column as class
            variable_columns = df.columns[:50]
            class_column = df.columns[-1]

            X = df[variable_columns]
            y = df[class_column]

            # Encode variables and class as discrete labels
            le = LabelEncoder()
            X_encoded = X.apply(lambda col: le.fit_transform(col.astype(str)), axis=0)
            y_encoded = le.fit_transform(y.astype(str))

            # Generate all unique pairs of variables
            variable_pairs = list(itertools.combinations(variable_columns, 2))

            # Initialize variable to track the maximum mutual information
            max_mi = -np.inf
            max_pair = (None, None)

            # Iterate over each pair and calculate mutual information
            for var1, var2 in variable_pairs:
                # Create a joint feature by combining the two variables
                joint_feature = X_encoded[var1].astype(str) + "_" + X_encoded[var2].astype(str)

                # Encode the joint feature
                joint_encoded = le.fit_transform(joint_feature)

                # Calculate mutual information between joint feature and class
                mi = mutual_info_score(joint_encoded, y_encoded)

                # Update maximum mutual information if current MI is higher
                if mi > max_mi:
                    max_mi = mi
                    max_pair = (var1, var2)

            # Append the result for the current file
            results.append({
                'Filename': os.path.basename(file_path),
                'MaxMutualInformation': max_mi,
                'Variable1': max_pair[0],
                'Variable2': max_pair[1]
            })

        except Exception as e:
            print(f"Error processing file {os.path.basename(file_path)}: {e}")
            continue  # Continue with the next file in case of error

    # Create a DataFrame from the results
    results_df = pd.DataFrame(results)

    # Save the results to the output CSV
    results_df.to_csv(output_csv, index=False, encoding='utf-8')

    print(f"Processing completed. Results saved to {output_csv}")


if __name__ == "__main__":
    # Define input and output paths
    input_directory = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position2\2_EDM-1_csv"
    output_csv = r"D:\1111山东大学的事\大三上\生物信息\2024秋课程设计\疾病位点识别\data\position2\2_EDM-1_csv\max_mutual_information_results.csv"

    # Call the function to compute and save the results
    compute_max_mutual_information(input_directory, output_csv)
