import csv
from collections import OrderedDict

def extract_unique_categories(csv_file):
    categories = set()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            categories.add(row['parent_category'])
            categories.add(row['child_category'])
    return categories

def write_nodes_csv(categories, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['category'])
        for category in categories:
            writer.writerow([category])

if __name__ == "__main__":
    input_csv_file = 'taxonomy_iw.csv'
    output_nodes_csv_file = 'nodes.csv'

    unique_categories = extract_unique_categories(input_csv_file)
    write_nodes_csv(unique_categories, output_nodes_csv_file)
