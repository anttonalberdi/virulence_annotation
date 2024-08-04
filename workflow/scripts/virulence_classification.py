import sys

input_table = sys.argv[1]
positive_domains_file = sys.argv[2]
negative_domains_file = sys.argv[3]
ambiguous_domains_file = sys.argv[4]
output_table = sys.argv[5]

# Read the positive domains into a set for fast lookup
with open(positive_domains_file, 'r') as domains_file:
    positive_domains = {line.strip() for line in domains_file}
        
# Read the negative domains into a set for fast lookup
with open(negative_domains_file, 'r') as domains_file:
    negative_domains = {line.strip() for line in domains_file}
        
# Read the ambiguous domains into a set for fast lookup
with open(ambiguous_domains_file, 'r') as domains_file:
    ambiguous_domains = {line.strip() for line in domains_file}
        
# Dictionary to store the results
results = {}

# Process the input table
with open(input_table, 'r') as infile:
    for line in infile:
        columns = line.strip().split()
        id_col1 = columns[0]
        domain = columns[1]

        if id_col1 not in results:
            results[id_col1] = {'positive': False, 'negative': False, 'ambiguous': False}

        if domain in positive_domains:
            results[id_col1]['positive'] = True
        elif domain in negative_domains:
            results[id_col1]['negative'] = True
        elif domain in ambiguous_domains:
            results[id_col1]['ambiguous'] = True

# Write the output table with the required format
with open(output_table, 'w') as outfile:
    for id_col1, flags in results.items():
        if flags['positive']:
            annotation = "positive"
        elif not flags['positive'] and flags['ambiguous']:
            annotation = "unclassified"
        elif flags['negative'] and not flags['positive'] and not flags['ambiguous']:
            annotation = "negative"
        else:
            annotation = "negative"

        outfile.write(f"{id_col1}\t{annotation}\n")
