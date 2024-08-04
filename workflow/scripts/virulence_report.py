import sys
import pandas as pd

# Load the TSV files
hmmer_df = pd.read_csv(sys.argv[1], sep='\t', header=None)
rf_df = pd.read_csv(sys.argv[2], sep='\t', header=None)
signalp_df = pd.read_csv(sys.argv[3], sep='\t', header=None)

# Keep only relevant columns
hmmer_df = hmmer_df[[0, 1]]
rf_df = rf_df[[1, 2]]
signalp_df = signalp_df[[0, 1]]

# Rename the columns for clarity
hmmer_df.columns = ['gene', 'hmmer']
rf_df.columns = ['gene', 'rf']
signalp_df.columns = ['gene', 'signalp']

# Merge the dataframes on the 'gene' column
merged_df = pd.merge(hmmer_df, rf_df, on='gene', how='outer')
merged_df = pd.merge(merged_df, signalp_df, on='gene', how='outer')

# Fill NaN values with 'NA' to denote missing data
merged_df = merged_df.fillna('NA')

# Define a function to determine the prediction value
def determine_prediction(row):
    hmmer = row['hmmer']
    rf = row['rf']
    signalp = row['signalp']
    
    if hmmer == 'pathogenic' and rf == 'pathogenic' and signalp != 'NA':
        return "1: Secreted Virulence factor"
    elif hmmer == 'unclassified' and rf == 'pathogenic' and signalp != 'NA':
        return "1: Secreted Virulence factor"
    elif hmmer == 'pathogenic' and rf == 'pathogenic' and signalp == 'NA':
        return "2: Non-secreted Virulence factor"
    elif hmmer == 'unclassified' and rf == 'pathogenic' and signalp == 'NA':
        return "2: Non-secreted Virulence factor"
    elif hmmer == 'negative' and rf == 'pathogenic' and signalp != 'NA':
        return "3: Potential Secreted Virulence factor"
    elif hmmer == 'NA' and rf == 'pathogenic' and signalp != 'NA':
        return "3: Potential Secreted Virulence factor"
    elif hmmer == 'pathogenic' and rf == 'negative' and signalp != 'NA':
        return "3: Potential Secreted Virulence factor"
    elif hmmer == 'negative' and rf == 'pathogenic' and signalp == 'NA':
        return "4: Potential Non-secreted Virulence factor"
    elif hmmer == 'NA' and rf == 'pathogenic' and signalp == 'NA':
        return "4: Potential Non-secreted Virulence factor"
    elif hmmer == 'pathogenic' and rf == 'negative' and signalp == 'NA':
        return "4: Potential Non-secreted Virulence factor"
    elif hmmer == 'negative' and rf == 'negative':
        return "-"
    else:
        return "NA"

# Apply the function to each row to create the 'prediction' column
merged_df['prediction'] = merged_df.apply(determine_prediction, axis=1)

# Sort the DataFrame by the 'Annotation' and 'Gene' columns
merged_df = merged_df.sort_values(by=['prediction', 'gene'])

# Output the final dataframe to a TSV file
merged_df.to_csv(sys.argv[4], sep='\t', index=False)
