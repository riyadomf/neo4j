import csv

input_file = 'taxonomy.csv'
output_file = 'taxonomy_preprocessed.csv'

with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
    reader = csv.reader(csv_in)
    writer = csv.writer(csv_out)
    for row in reader:
        # Remove escaped quotes from category names
        row = [col.replace('\"', '') for col in row]
        writer.writerow(row)
