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
        
with open(input_table, 'r') as infile, open(output_table, 'w') as outfile:
  for line in infile:
    columns = line.strip().split()
    annotation = ""
    if columns[1] in positive_domains:
      annotation = "pathogenic"
    elif columns[1] in negative_domains:
      annotation = "negative"
    elif columns[1] in ambiguous_domains:
      annotation = "ambiguous"
    # Write the original line with the appropriate annotation
    outfile.write(f"{line.strip()}\t{annotation}\n")
