import os
import pandas as pd
import glob
import sys

def calculate_statistics(file_list):
    # Define the columns for the output DataFrame
    output_columns = [
        "Sample", 
        "V1", 
        "V2", 
        "V3", 
        "V4", 
        "V5", 
        "AVI", 
        "NVI"
    ]
    # Create an empty DataFrame to store results
    results_df = pd.DataFrame(columns=output_columns)
    
    # Define the weights for the summatory index
    weights = {
        "V1": 1.0,
        "V2": 0.5,
        "V3": 0.2,
        "V4": 0.1,
        "V5": 0.0
    }
    
    for file_path in file_list:
        # Read the TSV file into a DataFrame
        df = pd.read_csv(file_path, sep='\t')
        
        # Count occurrences of each prediction value
        count_1 = (df['prediction'] == "1: Secreted Virulence factor").sum()
        count_2 = (df['prediction'] == "2: Non-secreted Virulence factor").sum()
        count_3 = (df['prediction'] == "3: Potential Secreted Virulence factor").sum()
        count_4 = (df['prediction'] == "4: Potential Non-secreted Virulence factor").sum()
        count_5 = (df['prediction'] == "5: Not a Virulence factor").sum()
        
        # Calculate the virulence index
        virulence_index = (
            count_1 * weights["V1"] +
            count_2 * weights["V2"] +
            count_3 * weights["V3"] +
            count_4 * weights["V4"] +
            count_5 * weights["V5"]
        )
        
        # Calculate the total number of rows
        total_rows = df.shape[0]
        
        # Calculate the normalized index
        normalised_index = virulence_index / total_rows * 100 if total_rows > 0 else 0

        # Extract the sample name without the .tsv extension
        sample_name = os.path.basename(file_path).replace('.tsv', '')
        
        # Append the results to the DataFrame
        results_df = results_df.append({
            "Sample": sample_name,
            "V1": count_1,
            "V2": count_2,
            "V3": count_3,
            "V4": count_4,
            "V5": count_5,
            "AVI": virulence_index,
            "NVI": normalised_index
        }, ignore_index=True)
    
    return results_df

def main(input_files, output_file):
    # Calculate statistics for each file
    results_df = calculate_statistics(input_files)
    
    # Save the results to a TSV file
    results_df.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    # Command line arguments: input files and output file
    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]
    
    main(input_files, output_file)
