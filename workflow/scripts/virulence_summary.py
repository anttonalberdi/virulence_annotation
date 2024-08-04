import os
import pandas as pd
import glob
import sys

def calculate_statistics(file_list):
    # Define the columns for the output DataFrame
    output_columns = [
        "Filename", 
        "Secreted Virulence factor", 
        "Non-secreted Virulence factor", 
        "Potential Secreted Virulence factor", 
        "Potential Non-secreted Virulence factor", 
        "Not a Virulence factor", 
        "Summatory Index", 
        "Normalized Index"
    ]
    # Create an empty DataFrame to store results
    results_df = pd.DataFrame(columns=output_columns)
    
    # Define the weights for the summatory index
    weights = {
        "1: Secreted Virulence factor": 1.0,
        "2: Non-secreted Virulence factor": 0.5,
        "3: Potential Secreted Virulence factor": 0.2,
        "4: Potential Non-secreted Virulence factor": 0.1,
        "5: Not a Virulence factor": 0.0
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
        
        # Calculate the summatory index
        summatory_index = (
            count_1 * weights["1: Secreted Virulence factor"] +
            count_2 * weights["2: Non-secreted Virulence factor"] +
            count_3 * weights["3: Potential Secreted Virulence factor"] +
            count_4 * weights["4: Potential Non-secreted Virulence factor"] +
            count_5 * weights["5: Not a Virulence factor"]
        )
        
        # Calculate the total number of rows
        total_rows = df.shape[0]
        
        # Calculate the normalized index
        normalized_index = summatory_index / total_rows if total_rows > 0 else 0
        
        # Append the results to the DataFrame
        results_df = results_df.append({
            "Filename": os.path.basename(file_path),
            "Secreted Virulence factor": count_1,
            "Non-secreted Virulence factor": count_2,
            "Potential Secreted Virulence factor": count_3,
            "Potential Non-secreted Virulence factor": count_4,
            "Not a Virulence factor": count_5,
            "Summatory Index": summatory_index,
            "Normalized Index": normalized_index
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
